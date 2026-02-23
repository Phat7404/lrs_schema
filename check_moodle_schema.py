import pymysql
from etl_app.config import settings

def check_schema():
    conn = pymysql.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=settings.mysql_database,
        cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cursor:
        cursor.execute("DESCRIBE mdl_competency_framework")
        print("\nTable: mdl_competency_framework")
        for row in cursor.fetchall():
            print(f"  {row['Field']}: {row['Type']}")
            
        cursor.execute("DESCRIBE mdl_competency")
        print("\nTable: mdl_competency")
        for row in cursor.fetchall():
            print(f"  {row['Field']}: {row['Type']}")
    conn.close()

if __name__ == "__main__":
    check_schema()
