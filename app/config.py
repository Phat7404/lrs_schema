from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # SQL Server (Data Warehouse) Configuration
    sqlserver_host: str = "localhost"
    sqlserver_port: int = 1433
    sqlserver_database: str = "moodle_datawarehouse"
    sqlserver_user: str = "SA"
    sqlserver_password: str = "Phat_07042004"
    
    # MySQL (Moodle) Configuration
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_database: str = "moodle"
    mysql_user: str = "root"
    mysql_password: str = "Phat_07042004"
    
    # xAPI LRS Configuration
    xapi_url: str = "https://cloud.scorm.com/lrs/W4B6LY6IO0/sandbox/statements"
    xapi_username: str = "W4B6LY6IO0"
    xapi_password: str = "1omfRe7QW2JtAI0F4Icv6ctQmmGJNjnhwYET72jp"
    
    # LMS Category Root (for bridge table)
    lms_category_root: str = "http://localhost/moodle"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

