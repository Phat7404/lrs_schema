import pymssql
import pymysql
from typing import Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections for SQL Server and MySQL"""
    
    def __init__(self):
        self.sqlserver_conn: Optional[pymssql.Connection] = None
        self.mysql_conn: Optional[pymysql.Connection] = None
    
    def get_sqlserver_connection(self):
        """Get or create SQL Server connection"""
        if self.sqlserver_conn is None or not self._is_connection_alive(self.sqlserver_conn):
            try:
                self.sqlserver_conn = pymssql.connect(
                    server=settings.sqlserver_host,
                    port=settings.sqlserver_port,
                    user=settings.sqlserver_user,
                    password=settings.sqlserver_password,
                    database=settings.sqlserver_database,
                    autocommit=False
                )
                logger.info("Connected to SQL Server")
            except Exception as e:
                logger.error(f"Error connecting to SQL Server: {e}")
                raise
        return self.sqlserver_conn
    
    def get_mysql_connection(self):
        """Get or create MySQL connection"""
        if self.mysql_conn is None or not self._is_mysql_connection_alive(self.mysql_conn):
            try:
                self.mysql_conn = pymysql.connect(
                    host=settings.mysql_host,
                    port=settings.mysql_port,
                    user=settings.mysql_user,
                    password=settings.mysql_password,
                    database=settings.mysql_database,
                    autocommit=False,
                    cursorclass=pymysql.cursors.DictCursor
                )
                logger.info("Connected to MySQL")
            except Exception as e:
                logger.error(f"Error connecting to MySQL: {e}")
                raise
        return self.mysql_conn
    
    def _is_connection_alive(self, conn) -> bool:
        """Check if SQL Server connection is alive"""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except:
            return False
    
    def _is_mysql_connection_alive(self, conn) -> bool:
        """Check if MySQL connection is alive"""
        try:
            conn.ping(reconnect=False)
            return True
        except:
            return False
    
    def close_all(self):
        """Close all database connections"""
        if self.sqlserver_conn:
            try:
                self.sqlserver_conn.close()
                logger.info("Closed SQL Server connection")
            except:
                pass
            self.sqlserver_conn = None
        
        if self.mysql_conn:
            try:
                self.mysql_conn.close()
                logger.info("Closed MySQL connection")
            except:
                pass
            self.mysql_conn = None

