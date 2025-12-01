import logging
from typing import Optional, Dict, Any
from app.database.connection import DatabaseManager

logger = logging.getLogger(__name__)


class MoodleService:
    """Service for fetching data from Moodle MySQL database"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from Moodle database
        
        Args:
            user_id: User ID or username
            
        Returns:
            Dictionary with user information or None
        """
        mysql_conn = self.db_manager.get_mysql_connection()
        if not mysql_conn:
            return None
        
        cursor = mysql_conn.cursor()
        try:
            cursor.execute("""
                SELECT id, username, firstname, lastname, email
                FROM mdl_user
                WHERE id = %s OR username = %s
                LIMIT 1
            """, (user_id, user_id))
            result = cursor.fetchone()
            return result
        except Exception as e:
            logger.warning(f"Could not fetch Moodle user info for {user_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def get_course_info(self, course_id: int) -> Optional[Dict[str, Any]]:
        """
        Get course information from Moodle database
        
        Args:
            course_id: Course ID
            
        Returns:
            Dictionary with course information or None
        """
        mysql_conn = self.db_manager.get_mysql_connection()
        if not mysql_conn or not course_id:
            return None
        
        cursor = mysql_conn.cursor()
        try:
            cursor.execute("""
                SELECT id, fullname, shortname, category
                FROM mdl_course
                WHERE id = %s
                LIMIT 1
            """, (course_id,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            logger.warning(f"Could not fetch Moodle course info for {course_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def get_module_info(self, module_id: int) -> Optional[Dict[str, Any]]:
        """
        Get module information from Moodle database
        
        Args:
            module_id: Module ID (cmid)
            
        Returns:
            Dictionary with module information or None
        """
        mysql_conn = self.db_manager.get_mysql_connection()
        if not mysql_conn or not module_id:
            return None
        
        cursor = mysql_conn.cursor()
        try:
            cursor.execute("""
                SELECT cm.id, cm.instance, cm.course, m.name as module_name
                FROM mdl_course_modules cm
                JOIN mdl_modules m ON cm.module = m.id
                WHERE cm.id = %s
                LIMIT 1
            """, (module_id,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            logger.warning(f"Could not fetch Moodle module info for {module_id}: {e}")
            return None
        finally:
            cursor.close()

