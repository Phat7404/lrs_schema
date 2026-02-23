from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # SQL Server (Data Warehouse) Configuration
    sqlserver_host: str = "localhost"
    sqlserver_port: int = 1433
    sqlserver_database: str = "xAPI_Analytics_DB"  # Updated to new DB name
    sqlserver_user: str = "SA"
    sqlserver_password: str = "Admin123"
    
    # MySQL (Moodle) Configuration
    mysql_host: str = "192.168.1.220"
    mysql_port: int = 3306
    mysql_database: str = "moodle_ubuntu"
    mysql_user: str = "root"
    mysql_password: str = "123"
    
    # xAPI LRS Configuration
    xapi_url: str = "https://cloud.scorm.com/lrs/IV2M3KSGCL/sandbox/statements"
    xapi_username: str = "IV2M3KSGCL"
    xapi_password: str = "1rCwrXheGPaOMq1XmEm0NWQjFnhBt8KjDIekEqQu"
    
    # LMS Category Root (for bridge table)
    lms_category_root: str = "http://localhost/moodle"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
