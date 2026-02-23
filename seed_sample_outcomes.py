import pymysql
from etl_app.config import settings
import time

def seed_sample_outcomes():
    """Seeds sample Learning Outcomes into Moodle database for testing ETL"""
    try:
        conn = pymysql.connect(
            host=settings.mysql_host,
            port=settings.mysql_port,
            user=settings.mysql_user,
            password=settings.mysql_password,
            database=settings.mysql_database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print(f"Connected to Moodle Database: {settings.mysql_database}")
        
        with conn.cursor() as cursor:
            # 1. Create Framework
            framework_idnumber = "DIST_SYS_2024"
            cursor.execute("SELECT id FROM mdl_competency_framework WHERE idnumber = %s", (framework_idnumber,))
            framework = cursor.fetchone()
            
            if not framework:
                sql_framework = """
                INSERT INTO mdl_competency_framework 
                (shortname, idnumber, description, descriptionformat, visible, scaleid, timecreated, timemodified, usermodified, contextid)
                VALUES (%s, %s, %s, 1, 1, 1, %s, %s, 2, 1)
                """
                now = int(time.time())
                cursor.execute(sql_framework, ("Hệ phân tán (Distributed Systems)", framework_idnumber, "Khung năng lực mẫu cho môn học Hệ phân tán", now, now))
                framework_id = conn.insert_id()
                print(f"Created Framework: {framework_idnumber}")
            else:
                framework_id = framework['id']
                print(f"Framework {framework_idnumber} already exists.")

            # 2. Define Sample Outcomes
            outcomes = [
                ("LO1", "LO1", "Students can **understand** the basic principles, models, and architectures of distributed systems."),
                ("LO2", "LO2", "Students can **apply** consistency models and synchronization algorithms in real-word scenarios."),
                ("LO3", "LO3", "Students can **analyze** performance metrics and identifying bottlenecks in large-scale services."),
                ("LO4", "LO4", "Students can **evaluate** security threats and mitigation strategies in decentralized environments."),
                ("LO5", "LO5", "Students can **create** and deploy a fault-tolerant distributed application using modern frameworks.")
            ]

            for sname, idnum, desc in outcomes:
                cursor.execute("SELECT id FROM mdl_competency WHERE idnumber = %s AND competencyframeworkid = %s", (idnum, framework_id))
                if not cursor.fetchone():
                    sql_lo = """
                    INSERT INTO mdl_competency 
                    (shortname, idnumber, description, descriptionformat, competencyframeworkid, parentid, path, sortorder, timecreated, timemodified, usermodified)
                    VALUES (%s, %s, %s, 1, %s, 0, '/0/', 0, %s, %s, 2)
                    """
                    cursor.execute(sql_lo, (sname, idnum, desc, framework_id, int(time.time()), int(time.time())))
                    print(f"  - Created Outcome: {idnum}")
                else:
                    print(f"  - Outcome {idnum} already exists.")

            conn.commit()
            print("\nSeeding completed successfully!")
            
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    seed_sample_outcomes()
