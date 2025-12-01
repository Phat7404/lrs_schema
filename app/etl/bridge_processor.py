import logging
from app.models.xapi_models import Statement
from app.database.connection import DatabaseManager
from app.config import settings

logger = logging.getLogger(__name__)


class BridgeProcessor:
    """Processes and loads bridge_ActivityHierarchy table (Closure Table)"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.sqlserver_conn = db_manager.get_sqlserver_connection()
    
    def process_activity_hierarchy(self, statement: Statement):
        """Process and insert bridge_ActivityHierarchy (Closure Table)"""
        activity_id = statement.object.id
        
        # Step 1: Self-reference (path_length = 0)
        self.insert_bridge_record(activity_id, activity_id, 0, False)
        
        # Step 2: Direct parent relationships
        if statement.context and statement.context.contextActivities:
            if statement.context.contextActivities.parent:
                for parent in statement.context.contextActivities.parent:
                    parent_id = parent.id
                    # Ensure parent exists in dim_activity
                    self.ensure_activity_exists(parent_id)
                    # Insert direct parent relationship
                    self.insert_bridge_record(parent_id, activity_id, 1, True)
                    
                    # Step 3: Indirect relationships (transitive closure)
                    self.build_closure_table(parent_id, activity_id)
        
        # Step 4: Add LMS Category root
        lms_root = settings.lms_category_root
        self.ensure_activity_exists(lms_root)
        # Find max path_length for this activity and add root with path_length + 1
        max_path = self.get_max_path_length(activity_id)
        self.insert_bridge_record(lms_root, activity_id, max_path + 1, False)
    
    def insert_bridge_record(self, ancestor_id: str, descendant_id: str, path_length: int, is_direct: bool):
        """Insert a record into bridge_ActivityHierarchy"""
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM bridge_ActivityHierarchy 
                              WHERE ancestor_activity_id = %s AND descendant_activity_id = %s)
                INSERT INTO bridge_ActivityHierarchy (ancestor_activity_id, descendant_activity_id, path_length, is_direct_parent)
                VALUES (%s, %s, %s, %s)
            """, (ancestor_id, descendant_id, ancestor_id, descendant_id, path_length, 1 if is_direct else 0))
        except Exception as e:
            logger.error(f"Error inserting bridge record: {e}")
        finally:
            cursor.close()
    
    def ensure_activity_exists(self, activity_id: str):
        """Ensure an activity exists in dim_activity"""
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_activity WHERE activity_id = %s)
                INSERT INTO dim_activity (activity_id, activity_url, is_category)
                VALUES (%s, %s, 0)
            """, (activity_id, activity_id, activity_id))
        except Exception as e:
            logger.error(f"Error ensuring activity exists: {e}")
        finally:
            cursor.close()
    
    def build_closure_table(self, ancestor_id: str, descendant_id: str):
        """Build transitive closure relationships"""
        cursor = self.sqlserver_conn.cursor()
        try:
            # Find all ancestors of the ancestor
            cursor.execute("""
                SELECT ancestor_activity_id, path_length
                FROM bridge_ActivityHierarchy
                WHERE descendant_activity_id = %s
            """, (ancestor_id,))
            
            for row in cursor.fetchall():
                grand_ancestor = row[0]
                ancestor_path = row[1]
                new_path_length = ancestor_path + 1
                self.insert_bridge_record(grand_ancestor, descendant_id, new_path_length, False)
        except Exception as e:
            logger.error(f"Error building closure table: {e}")
        finally:
            cursor.close()
    
    def get_max_path_length(self, activity_id: str) -> int:
        """Get maximum path_length for an activity"""
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                SELECT MAX(path_length) as max_path
                FROM bridge_ActivityHierarchy
                WHERE descendant_activity_id = %s
            """, (activity_id,))
            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else 0
        except Exception as e:
            logger.error(f"Error getting max path length: {e}")
            return 0
        finally:
            cursor.close()

