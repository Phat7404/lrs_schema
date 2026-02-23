import logging
from datetime import datetime
from etl_app.models.xapi_models import Statement
from etl_app.database.connection import DatabaseManager
from etl_app.etl.utils import DataExtractor

logger = logging.getLogger(__name__)


class FactProcessor:
    """Processes and loads fact tables for the new schema"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.sqlserver_conn = db_manager.get_sqlserver_connection()
        self.extractor = DataExtractor()
        
    def process_fact_statement(self, statement: Statement, time_id: int, context_id: str):
        """Process fact_statement"""
        event_id = statement.id
        actor_id = statement.actor.account.name if statement.actor.account else None
        full_verb_id = statement.verb.id
        interaction_id = full_verb_id.strip('/').split('/')[-1]
        
        timestamp = self.extractor.parse_timestamp(statement.timestamp)
        object_type = statement.object.objectType
        object_id = statement.object.id
        
        # Extract Result data
        # result_flag: 1 if success, 0 otherwise (fail or no result)
        result_flag = 1 if statement.result and statement.result.success is True else 0
        raw_duration_ms = None
        if statement.result and statement.result.duration:
            duration_sec = self.extractor.parse_duration(statement.result.duration)
            if duration_sec is not None:
                raw_duration_ms = duration_sec * 1000

        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM fact_statement WHERE event_id = %s)
                INSERT INTO fact_statement (event_id, actor_id, interaction_id, context_id, [timestamp], object_type, object_id, result_flag, raw_duration_ms, time_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (event_id, event_id, actor_id, interaction_id, context_id, timestamp, object_type, object_id, result_flag, raw_duration_ms, time_id))
        except Exception as e:
            logger.error(f"Error processing fact_statement: {e}")
        finally:
            cursor.close()

    def process_fact_session(self, statement: Statement, time_id: int, context_id: str):
        """Process fact_session based on registration (session_id)"""
        if not statement.context or not statement.context.registration:
            return
            
        session_id = statement.context.registration
        actor_id = statement.actor.account.name if statement.actor.account else None
        timestamp = self.extractor.parse_timestamp(statement.timestamp)
        
        # 1. Simplify Entry Point (e.g., extracting 'quiz', 'course', 'page')
        full_object_id = statement.object.id
        entry_point = "other"
        if 'quiz' in full_object_id.lower():
            entry_point = "quiz"
        elif 'course' in full_object_id.lower():
            entry_point = "course"
        elif 'page' in full_object_id.lower():
            entry_point = "page"
        elif 'resource' in full_object_id.lower():
            entry_point = "resource"
            
        # 2. Context ID is passed from outside
        
        # 3. Default session type
        session_type = "learning"

        cursor = self.sqlserver_conn.cursor()
        try:
            # Update existing session or insert new
            cursor.execute("""
                IF EXISTS (SELECT 1 FROM fact_session WHERE session_id = %s)
                BEGIN
                    UPDATE fact_session 
                    SET end_time = %s, 
                        session_duration = DATEDIFF(second, start_time, %s),
                        context_id = %s
                    WHERE session_id = %s AND end_time < %s
                END
                ELSE
                BEGIN
                    INSERT INTO fact_session (session_id, actor_id, entry_point, session_type, start_time, end_time, session_duration, context_id, time_id)
                    VALUES (%s, %s, %s, %s, %s, %s, 0, %s, %s)
                END
            """, (session_id, timestamp, timestamp, context_id, session_id, timestamp, 
                  session_id, actor_id, entry_point, session_type, timestamp, timestamp, context_id, time_id))
        except Exception as e:
            logger.error(f"Error processing fact_session: {e}")
        finally:
            cursor.close()

    def _get_quiz_metadata(self, cmid, actor_id):
        """Fetch max_score and attempt_no from Moodle"""
        max_score = None
        attempt_no = None
        
        if not cmid:
            return None, None
            
        try:
            mysql_conn = self.db_manager.get_mysql_connection()
            with mysql_conn.cursor() as mysql_cursor:
                # Get quiz instance ID and max grade
                mysql_cursor.execute("""
                    SELECT cm.instance, q.grade as max_score
                    FROM mdl_course_modules cm
                    JOIN mdl_quiz q ON q.id = cm.instance
                    WHERE cm.id = %s
                """, (cmid,))
                res = mysql_cursor.fetchone()
                
                if res:
                    max_score = res['max_score']
                    quiz_instance = res['instance']
                    
                    # Get attempt number for this user
                    if actor_id:
                        mysql_cursor.execute("""
                            SELECT MAX(attempt) as attempt_no 
                            FROM mdl_quiz_attempts 
                            WHERE quiz = %s AND userid = (
                                SELECT id FROM mdl_user WHERE username = %s OR id = %s
                            )
                        """, (quiz_instance, actor_id, actor_id))
                        att_res = mysql_cursor.fetchone()
                        if att_res and att_res['attempt_no']:
                            attempt_no = att_res['attempt_no']
                            
        except Exception as e:
            logger.error(f"Error fetching quiz metadata from Moodle: {e}")
            
        return max_score, attempt_no

    def _generate_quiz_attempt_id(self, statement: Statement) -> str:
        """Generate a unique quiz_attempt_id from registration + quiz cmid"""
        registration = statement.context.registration if statement.context else "no_reg"
        cmid = self.extractor.extract_moodle_module_id(statement.object.id)
        
        # User requested explicitly: combine registration + cmid
        if cmid:
            raw = f"{registration}_{cmid}"
        else:
            # Fallback if cmid is missing
            raw = f"{registration}_{statement.object.id}"
            
        return str(self.extractor.normalize_uuid(raw))

    def _upsert_quiz_record(self, quiz_attempt_id, time_id, actor_id, timestamp=None, 
                          total_score=None, max_score=None, is_complete=None, is_succeed=None, 
                          duration_ms=None, attempt_no=None):
        """Helper to insert or update fact_quiz record"""
        cursor = self.sqlserver_conn.cursor()
        try:
            # Check if record exists
            cursor.execute("SELECT 1 FROM fact_quiz WHERE quiz_attempt_id = %s", (quiz_attempt_id,))
            exists = cursor.fetchone()

            if exists:
                # Update existing record with available fields
                query_parts = []
                params = []
                
                if total_score is not None:
                    query_parts.append("total_score = %s")
                    params.append(total_score)
                if max_score is not None:
                    query_parts.append("max_score = %s")
                    params.append(max_score)
                if is_complete is not None:
                    query_parts.append("isComplete = %s")
                    params.append(1 if is_complete else 0)
                if is_succeed is not None:
                    query_parts.append("isSucceed = %s")
                    params.append(1 if is_succeed else 0)
                if duration_ms is not None:
                    query_parts.append("raw_duration_ms = %s")
                    params.append(duration_ms)
                if attempt_no is not None:
                    query_parts.append("attempt_no = %s")
                    params.append(attempt_no)
                if timestamp and is_complete: 
                    query_parts.append("end_time = %s")
                    params.append(timestamp)
                
                if query_parts:
                    sql = f"UPDATE fact_quiz SET {', '.join(query_parts)} WHERE quiz_attempt_id = %s"
                    params.append(quiz_attempt_id)
                    cursor.execute(sql, tuple(params))
            else:
                # Insert new record
                fields = ["quiz_attempt_id", "actor_id", "time_id"]
                values = ["%s", "%s", "%s"]
                params = [quiz_attempt_id, actor_id, time_id]
                
                if timestamp:
                    if is_complete:
                        fields.append("end_time")
                    else:
                        fields.append("start_time")
                    values.append("%s")
                    params.append(timestamp)
                    
                if max_score is not None:
                    fields.append("max_score")
                    values.append("%s")
                    params.append(max_score)
                if attempt_no is not None:
                    fields.append("attempt_no")
                    values.append("%s")
                    params.append(attempt_no)
                if total_score is not None:
                    fields.append("total_score")
                    values.append("%s")
                    params.append(total_score)
                if is_complete is not None:
                    fields.append("isComplete")
                    values.append("%s")
                    params.append(1 if is_complete else 0)
                if is_succeed is not None:
                    fields.append("isSucceed")
                    values.append("%s")
                    params.append(1 if is_succeed else 0)
                if duration_ms is not None:
                    fields.append("raw_duration_ms")
                    values.append("%s")
                    params.append(duration_ms)
                    
                sql = f"INSERT INTO fact_quiz ({', '.join(fields)}) VALUES ({', '.join(values)})"
                cursor.execute(sql, tuple(params))
                
        except Exception as e:
            logger.error(f"Error upserting fact_quiz: {e}")
        finally:
            cursor.close()

    def process_fact_quiz(self, statement: Statement, time_id: int):
        """Process fact_quiz for quiz-related verbs (completed/passed/failed/started)"""
        verb_id = statement.verb.id.lower()
        object_id = statement.object.id.lower()
        
        # Only process quiz-related statements
        if 'quiz' not in object_id:
            return
            
        is_completion = any(v in verb_id for v in ['completed', 'passed', 'failed'])
        is_start = 'start' in verb_id
        
        if not is_completion and not is_start:
            return
            
        if not statement.context or not statement.context.registration:
            return
            
        quiz_attempt_id = self._generate_quiz_attempt_id(statement)
        actor_id = statement.actor.account.name if statement.actor.account else None
        timestamp = self.extractor.parse_timestamp(statement.timestamp)
        cmid = self.extractor.extract_moodle_module_id(statement.object.id)
        
        # Extract result data
        total_score = None
        is_complete = None
        is_succeed = None
        duration_ms = None
        
        if statement.result:
            if statement.result.score:
                total_score = statement.result.score.raw
            if statement.result.completion is not None:
                is_complete = statement.result.completion
            if statement.result.success is not None:
                is_succeed = statement.result.success
            dur = self.extractor.parse_duration(statement.result.duration)
            if dur: duration_ms = dur * 1000

        # Refine flags based on verb if missing
        if 'completed' in verb_id and is_complete is None: is_complete = True
        if 'passed' in verb_id and is_succeed is None: is_succeed = True
        if 'failed' in verb_id and is_succeed is None: is_succeed = False

        # Fetch max_score and attempt_no from Moodle
        max_score, attempt_no = self._get_quiz_metadata(cmid, actor_id)

        # Upsert
        self._upsert_quiz_record(
            quiz_attempt_id=quiz_attempt_id,
            time_id=time_id,
            actor_id=actor_id,
            timestamp=timestamp,
            total_score=total_score,
            max_score=max_score,
            is_complete=is_complete,
            is_succeed=is_succeed,
            duration_ms=duration_ms,
            attempt_no=attempt_no
        )

    def process_fact_question(self, statement: Statement, time_id: int):
        """Process fact_question for answered verbs"""
        if 'answered' not in statement.verb.id.lower() or not statement.context or not statement.context.registration:
            return
        
        # Only process quiz questions
        if 'quiz' not in statement.object.id.lower():
            return
            
        question_id = statement.object.id
        actor_id = statement.actor.account.name if statement.actor.account else None
        
        # 1. Generate quiz_attempt_id
        quiz_attempt_id = self._generate_quiz_attempt_id(statement)
        
        # 2. Extract metadata for the parent quiz
        cmid = self.extractor.extract_moodle_module_id(statement.object.id)
        max_score, attempt_no = self._get_quiz_metadata(cmid, actor_id)
        
        # 3. Ensure parent quiz exists (Rich Upsert)
        start_time = self.extractor.parse_timestamp(statement.timestamp)
        
        self._upsert_quiz_record(
            quiz_attempt_id=quiz_attempt_id,
            time_id=time_id,
            actor_id=actor_id,
            timestamp=start_time, # Start time approximation
            max_score=max_score,
            attempt_no=attempt_no,
            is_complete=False 
        )

        selected_answer = statement.result.response if statement.result else None
        is_correct = statement.result.success if statement.result else None

        # Insert question record
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM fact_question WHERE question_id = %s AND quiz_attempt_id = %s)
                INSERT INTO fact_question (question_id, quiz_attempt_id, selected_answer, is_correct)
                VALUES (%s, %s, %s, %s)
            """, (question_id, quiz_attempt_id, question_id, quiz_attempt_id, selected_answer, 1 if is_correct else 0))
        except Exception as e:
            logger.error(f"Error processing fact_question: {e}")
        finally:
            cursor.close()


    def process_fact_activity(self, statement: Statement, time_id: int, context_id: str):
        """Process fact_activity summary with Moodle metadata"""
        activity_id = statement.object.id
        actor_id = statement.actor.account.name if statement.actor.account else None
        activity_type = statement.object.definition.type if statement.object.definition else None
        
        # 1. Logic for completion_status
        completion_status = "In Progress"
        if statement.result:
            if statement.result.completion:
                completion_status = "Completed"
            if statement.result.success is True:
                completion_status = "Passed"
            elif statement.result.success is False:
                completion_status = "Failed"

        # 2. Extract Duration
        duration = 0
        if statement.result and statement.result.duration:
            duration = self.extractor.parse_duration(statement.result.duration) or 0
        
        # 3. Fetch Moodle Metadata (activity_length, activity_order, is_mandatory)
        activity_length = None
        activity_order = None
        is_mandatory = 1
        
        cmid = self.extractor.extract_moodle_module_id(activity_id)
        if cmid:
            try:
                mysql_conn = self.db_manager.get_mysql_connection()
                with mysql_conn.cursor() as mysql_cursor:
                    # Generic query to get module info
                    mysql_cursor.execute("""
                        SELECT cm.section, cm.completion, cm.added
                        FROM mdl_course_modules cm
                        WHERE cm.id = %s
                    """, (cmid,))
                    res = mysql_cursor.fetchone()
                    if res:
                        activity_order = res['section']
                        is_mandatory = 1 if res['completion'] > 0 else 0
            except Exception as e:
                logger.error(f"Error fetching activity metadata from Moodle: {e}")

        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF EXISTS (SELECT 1 FROM fact_activity WHERE activity_id = %s AND actor_id = %s AND time_id = %s)
                BEGIN
                    UPDATE fact_activity 
                    SET time_spent = time_spent + %s,
                        attempt_count = attempt_count + 1,
                        completion_status = %s
                    WHERE activity_id = %s AND actor_id = %s AND time_id = %s
                END
                ELSE
                BEGIN
                    INSERT INTO fact_activity (activity_id, actor_id, time_spent, attempt_count, context_id, time_id, 
                                             activity_type, activity_length, activity_order, is_mandatory, completion_status)
                    VALUES (%s, %s, %s, 1, %s, %s, %s, %s, %s, %s, %s)
                END
            """, (activity_id, actor_id, time_id, duration, completion_status, activity_id, actor_id, time_id,
                  activity_id, actor_id, duration, context_id, time_id, activity_type, 
                  activity_length, activity_order, is_mandatory, completion_status))
        except Exception as e:
            logger.error(f"Error processing fact_activity: {e}")
        finally:
            cursor.close()

    def process_fact_progress(self, statement: Statement, context_id: str):
        """Process fact_progress based on completion or outcomes"""
        if not statement.result or not statement.result.completion:
            return
            
        actor_id = statement.actor.account.name if statement.actor.account else None
        last_time = self.extractor.parse_timestamp(statement.timestamp)
        
        # 1. Look for outcome_id in extensions
        outcome_ids = []
        if statement.context and statement.context.extensions:
            for key, val in statement.context.extensions.items():
                if 'outcome' in key.lower():
                    outcome_ids.append(str(val))
                    break
        
        # 2. Fallback: Search in Moodle if not in xAPI
        if not outcome_ids:
            cmid = self.extractor.extract_moodle_module_id(statement.object.id)
            if cmid:
                try:
                    mysql_conn = self.db_manager.get_mysql_connection()
                    with mysql_conn.cursor() as mysql_cursor:
                        mysql_cursor.execute("SELECT competencyid FROM mdl_competency_modulecomp WHERE cmid = %s", (cmid,))
                        results = mysql_cursor.fetchall()
                        for row in results:
                            outcome_ids.append(str(row['competencyid']))
                except Exception as e:
                    logger.error(f"Error finding outcomes for progress: {e}")

        if not outcome_ids: return

        cursor = self.sqlserver_conn.cursor()
        try:
            for outcome_id in outcome_ids:
                cursor.execute("""
                    INSERT INTO fact_progress (actor_id, outcome_id, progress_percent, last_activity_time, context_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (actor_id, outcome_id, 100.0, last_time, context_id))
        except Exception as e:
            logger.error(f"Error processing fact_progress: {e}")
        finally:
            cursor.close()

    def process_all(self, statement: Statement, time_id: int, context_id: str):
        """Process all relevant fact tables"""
        self.process_fact_statement(statement, time_id, context_id)
        self.process_fact_session(statement, time_id, context_id)
        self.process_fact_quiz(statement, time_id)
        self.process_fact_question(statement, time_id)
        self.process_fact_activity(statement, time_id, context_id)
        self.process_fact_progress(statement, context_id)
