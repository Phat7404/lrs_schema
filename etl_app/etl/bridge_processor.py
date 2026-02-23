import logging
from etl_app.models.xapi_models import Statement
from etl_app.database.connection import DatabaseManager

logger = logging.getLogger(__name__)


class BridgeProcessor:
    """Processes and loads bridge_ActivityHierachy table (Closure Table)"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.sqlserver_conn = db_manager.get_sqlserver_connection()
    
    def process_activity_hierarchy(self, statement: Statement):
        """Process and insert bridge_ActivityHierachy (Closure Table)"""
        activity_id = statement.object.id
        
        # Ensure descendant exists
        self.ensure_activity_exists(activity_id)
        
        # 1. Self-reference
        self.insert_bridge_record(activity_id, activity_id, 0)
        
        # 2. Parent relationships
        if statement.context and statement.context.contextActivities:
            if statement.context.contextActivities.parent:
                for parent in statement.context.contextActivities.parent:
                    # Ensure ancestor exists
                    self.ensure_activity_exists(parent.id)
                    self.insert_bridge_record(parent.id, activity_id, 1)

    def ensure_activity_exists(self, activity_id: str):
        """Ensure an activity exists in dim_activity to satisfy FK constraints"""
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_activity WHERE activity_id = %s)
                INSERT INTO dim_activity (activity_id)
                VALUES (%s)
            """, (activity_id, activity_id))
        except Exception as e:
            logger.error(f"Error ensuring activity exists {activity_id}: {e}")
        finally:
            cursor.close()

    def insert_bridge_record(self, ancestor_id: str, descendant_id: str, is_direct: int):
        """Insert a record into bridge_ActivityHierachy"""
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM bridge_ActivityHierachy 
                              WHERE ancestor_activity_id = %s AND descendant_activity = %s)
                INSERT INTO bridge_ActivityHierachy (ancestor_activity_id, descendant_activity, is_direct_parent)
                VALUES (%s, %s, %s)
            """, (ancestor_id, descendant_id, ancestor_id, descendant_id, is_direct))
        except Exception as e:
            logger.error(f"Error inserting bridge record: {e}")
        finally:
            cursor.close()
