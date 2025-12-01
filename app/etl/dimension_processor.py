import hashlib
import logging
from typing import Optional
from app.models.xapi_models import Statement
from app.database.connection import DatabaseManager
from app.etl.utils import DataExtractor

logger = logging.getLogger(__name__)


class DimensionProcessor:
    """Processes and loads dimension tables"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.sqlserver_conn = db_manager.get_sqlserver_connection()
        self.extractor = DataExtractor()
    
    def process_actor_account(self, statement: Statement):
        """Process and insert/update dim_actor_account"""
        if not statement.actor.account:
            return
        
        actor_account_id = statement.actor.account.name
        actor_home_page = statement.actor.account.homePage
        actor_name = statement.actor.name
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_actor_account WHERE actor_account_id = %s)
                INSERT INTO dim_actor_account (actor_account_id, actor_home_page, actor_name)
                VALUES (%s, %s, %s)
            """, (actor_account_id, actor_account_id, actor_home_page, actor_name))
        except Exception as e:
            logger.error(f"Error processing dim_actor_account: {e}")
        finally:
            cursor.close()
    
    def process_verb(self, statement: Statement):
        """Process and insert/update dim_verb"""
        verb_id = statement.verb.id
        verb_display = statement.verb.display.en if statement.verb.display else None
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_verb WHERE verb_id = %s)
                INSERT INTO dim_verb (verb_id, verb_display)
                VALUES (%s, %s)
            """, (verb_id, verb_id, verb_display))
        except Exception as e:
            logger.error(f"Error processing dim_verb: {e}")
        finally:
            cursor.close()
    
    def process_activity(self, statement: Statement):
        """Process and insert/update dim_activity"""
        activity_id = statement.object.id
        activity_url = activity_id
        is_category = False
        
        # Check if it's a category from contextActivities
        if statement.context and statement.context.contextActivities:
            if statement.context.contextActivities.category:
                is_category = True
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_activity WHERE activity_id = %s)
                INSERT INTO dim_activity (activity_id, activity_url, is_category)
                VALUES (%s, %s, %s)
            """, (activity_id, activity_id, activity_url, is_category))
        except Exception as e:
            logger.error(f"Error processing dim_activity: {e}")
        finally:
            cursor.close()
    
    def process_activity_detail(self, statement: Statement):
        """Process and insert/update activity_detail"""
        activity_id = statement.object.id
        activity_name = None
        activity_type_uri = None
        object_type = statement.object.objectType
        
        if statement.object.definition:
            if statement.object.definition.name:
                activity_name = statement.object.definition.name.get('en')
            activity_type_uri = statement.object.definition.type
        
        # Extract moodle_module_id and moodle_course_id from URLs
        moodle_module_id = self.extractor.extract_moodle_module_id(activity_id)
        moodle_course_id = self.extractor.extract_moodle_course_id(statement)
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM activity_detail WHERE activity_id = %s)
                INSERT INTO activity_detail (activity_id, activity_name, activity_type_uri, object_type, moodle_module_id, moodle_course_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (activity_id, activity_id, activity_name, activity_type_uri, object_type, moodle_module_id, moodle_course_id))
        except Exception as e:
            logger.error(f"Error processing activity_detail: {e}")
        finally:
            cursor.close()
    
    def process_event_meta(self, statement: Statement):
        """Process and insert/update dim_event_meta"""
        event_name = self.extractor.extract_event_name(statement)
        if not event_name:
            return
        
        # Create hash of event_name
        event_meta_id = hashlib.md5(event_name.encode()).hexdigest()
        
        # Parse moodle_event_action and moodle_module_name
        moodle_event_action = event_name.split('\\')[-1] if '\\' in event_name else event_name.split('/')[-1]
        moodle_module_name = event_name.split('\\')[0] if '\\' in event_name else event_name.split('/')[0]
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_event_meta WHERE event_meta_id = %s)
                INSERT INTO dim_event_meta (event_meta_id, moodle_event_action, moodle_module_name)
                VALUES (%s, %s, %s)
            """, (event_meta_id, event_meta_id, moodle_event_action, moodle_module_name))
        except Exception as e:
            logger.error(f"Error processing dim_event_meta: {e}")
        finally:
            cursor.close()
    
    def process_all_dimensions(self, statement: Statement):
        """Process all dimension tables for a statement"""
        self.process_actor_account(statement)
        self.process_verb(statement)
        self.process_activity(statement)
        self.process_activity_detail(statement)
        self.process_event_meta(statement)

