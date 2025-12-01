import hashlib
import logging
import uuid
from typing import Optional, Tuple
from datetime import datetime
from app.models.xapi_models import Statement
from app.database.connection import DatabaseManager
from app.etl.utils import DataExtractor

logger = logging.getLogger(__name__)


class FactProcessor:
    """Processes and loads fact tables"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.sqlserver_conn = db_manager.get_sqlserver_connection()
        self.extractor = DataExtractor()
    
    def process_statement(self, statement: Statement, stmt_id: str):
        """Process and insert fact_statement"""
        if not statement.actor.account:
            return
        
        actor_account_id = statement.actor.account.name
        verb_id = statement.verb.id
        activity_id = statement.object.id
        
        # Extract event_meta_id
        event_meta_id = None
        event_name = self.extractor.extract_event_name(statement)
        if event_name:
            event_meta_id = hashlib.md5(event_name.encode()).hexdigest()
        
        moodle_module_id = self.extractor.extract_moodle_module_id(activity_id)
        registration_id = statement.context.registration if statement.context else None
        
        # Convert registration_id to UUID format if present
        registration_id = self.extractor.normalize_uuid(registration_id)
        
        # Parse timestamps
        event_timestamp = self.extractor.parse_timestamp(statement.timestamp)
        stored_timestamp = self.extractor.parse_timestamp(statement.stored)
        ingest_timestamp = datetime.now()
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM fact_statement WHERE statement_id = %s)
                INSERT INTO fact_statement (statement_id, actor_account_id, verb_id, activity_id, event_meta_id, 
                                          moodle_module_id, registration_id, event_timestamp, stored_timestamp, ingest_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (stmt_id, stmt_id, actor_account_id, verb_id, activity_id, event_meta_id, 
                  moodle_module_id, registration_id, event_timestamp, stored_timestamp, ingest_timestamp))
        except Exception as e:
            logger.error(f"Error processing fact_statement: {e}")
        finally:
            cursor.close()
    
    def process_quiz(self, statement: Statement, stmt_id: str):
        """Process and insert fact_quiz"""
        if not statement.result:
            return
        
        # Extract duration (convert ISO 8601 duration to seconds)
        duration = self.extractor.parse_duration(statement.result.duration)
        
        # Calculate attempt_count (count statements with 'started' verb for same actor/activity)
        attempt_count = self._calculate_attempt_count(statement)
        
        # Extract score
        score_raw = None
        if statement.result.score:
            score_raw = statement.result.score.raw or statement.result.score.scaled
        
        # Extract quiz_name and module_name from contextActivities
        quiz_name = None
        module_name = None
        if statement.context and statement.context.contextActivities:
            if statement.context.contextActivities.parent:
                for parent in statement.context.contextActivities.parent:
                    if parent.definition and parent.definition.name:
                        name = parent.definition.name.get('en')
                        if not quiz_name:
                            quiz_name = name
                        module_name = name
        
        is_completed = statement.result.completion or False
        is_successful = statement.result.success
        
        # Calculate review information
        is_reviewed, review_count, last_review_timestamp = self._calculate_review_info(statement)
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM fact_quiz WHERE statement_id = %s)
                INSERT INTO fact_quiz (statement_id, duration, attempt_count, score_raw, quiz_name, is_completed, 
                                     is_successful, module_name, is_reviewed, review_count, last_review_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (stmt_id, stmt_id, duration, attempt_count, score_raw, quiz_name, is_completed, 
                  is_successful, module_name, is_reviewed, review_count, last_review_timestamp))
        except Exception as e:
            logger.error(f"Error processing fact_quiz: {e}")
        finally:
            cursor.close()
    
    def process_question_answer(self, statement: Statement, stmt_id: str):
        """Process and insert fact_question_answer"""
        if not statement.result:
            return
        
        question_activity_id = statement.object.id
        response_pattern = statement.result.response
        is_correct = statement.result.success
        
        correct_answer_pattern = None
        if statement.object.definition and statement.object.definition.correctResponsesPattern:
            correct_answer_pattern = ','.join(statement.object.definition.correctResponsesPattern)
        
        score_raw = None
        if statement.result.score:
            score_raw = statement.result.score.raw
        
        # Extract attempt_activity_id from contextActivities.parent
        attempt_activity_id = None
        if statement.context and statement.context.contextActivities:
            if statement.context.contextActivities.parent:
                for parent in statement.context.contextActivities.parent:
                    if 'attempt' in parent.id.lower():
                        attempt_activity_id = parent.id
                        break
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM fact_question_answer WHERE statement_id = %s)
                INSERT INTO fact_question_answer (statement_id, question_activity_id, response_pattern, is_correct, 
                                                 correct_answer_pattern, score_raw, attempt_activity_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (stmt_id, stmt_id, question_activity_id, response_pattern, is_correct, 
                  correct_answer_pattern, score_raw, attempt_activity_id))
        except Exception as e:
            logger.error(f"Error processing fact_question_answer: {e}")
        finally:
            cursor.close()
    
    def _calculate_attempt_count(self, statement: Statement) -> Optional[int]:
        """Calculate attempt count for a quiz"""
        if not statement.actor.account or not statement.object.id:
            return None
        
        actor_account_id = statement.actor.account.name
        activity_id = statement.object.id
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) as attempt_count
                FROM fact_statement
                WHERE actor_account_id = %s
                  AND activity_id = %s
                  AND verb_id LIKE %s
            """, (actor_account_id, activity_id, '%started%'))
            result = cursor.fetchone()
            return result[0] + 1 if result else 1  # +1 for current attempt
        except Exception as e:
            logger.error(f"Error calculating attempt count: {e}")
            return 1
        finally:
            cursor.close()
    
    def _calculate_review_info(self, statement: Statement) -> Tuple[bool, int, Optional[datetime]]:
        """Calculate review information for a quiz"""
        if not statement.actor.account or not statement.object.id:
            return False, 0, None
        
        actor_account_id = statement.actor.account.name
        activity_id = statement.object.id
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) as review_count, MAX(event_timestamp) as last_review
                FROM fact_statement
                WHERE actor_account_id = %s
                  AND activity_id = %s
                  AND verb_id LIKE %s
            """, (actor_account_id, activity_id, '%review%'))
            result = cursor.fetchone()
            review_count = result[0] if result and result[0] else 0
            last_review = result[1] if result and result[1] else None
            is_reviewed = review_count > 0
            return is_reviewed, review_count, last_review
        except Exception as e:
            logger.error(f"Error calculating review info: {e}")
            return False, 0, None
        finally:
            cursor.close()

