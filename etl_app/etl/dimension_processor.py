import logging
from typing import Optional
from etl_app.models.xapi_models import Statement
from etl_app.database.connection import DatabaseManager
from etl_app.etl.utils import DataExtractor

logger = logging.getLogger(__name__)


class DimensionProcessor:
    """Processes and loads dimension tables for the new schema"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.sqlserver_conn = db_manager.get_sqlserver_connection()
        self.extractor = DataExtractor()
    
    def process_actor(self, statement: Statement):
        """Process and insert/update dim_actor"""
        actor_id = None
        if statement.actor.account:
            actor_id = statement.actor.account.name
        
        if not actor_id:
            return
            
        actor_name = statement.actor.name
        
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_actor WHERE actor_id = %s)
                INSERT INTO dim_actor (actor_id, actor_name)
                VALUES (%s, %s)
                ELSE
                UPDATE dim_actor SET actor_name = %s WHERE actor_id = %s
            """, (actor_id, actor_id, actor_name, actor_name, actor_id))
        except Exception as e:
            logger.error(f"Error processing dim_actor: {e}")
        finally:
            cursor.close()
    
    def process_interaction_type(self, statement: Statement):
        """Process and insert/update dim_interation_type using a simplified ID"""
        full_verb_id = statement.verb.id
        # Extract the last part of the URL (e.g., 'completed' from '.../verbs/completed')
        interaction_id = full_verb_id.strip('/').split('/')[-1]
        
        interaction_name = statement.verb.display.en if statement.verb.display else interaction_id.capitalize()
        
        # Refined categorization logic to reduce "Other"
        category = "Other"
        v_id = interaction_id.lower()
        
        if any(x in v_id for x in ['launched', 'start', 'viewed']): category = "navigation"
        elif any(x in v_id for x in ['experienced', 'receive']): category = "engagement"
        elif any(x in v_id for x in ['answered', 'passed', 'failed']): category = "assessment"
        elif any(x in v_id for x in ['completed', 'uncompleted']): category = "completion"

        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_interation_type WHERE interaction_id = %s)
                INSERT INTO dim_interation_type (interaction_id, interaction_name, interaction_category)
                VALUES (%s, %s, %s)
                ELSE
                UPDATE dim_interation_type 
                SET interaction_category = %s, interaction_name = %s
                WHERE interaction_id = %s
            """, (interaction_id, interaction_id, interaction_name, category, category, interaction_name, interaction_id))
        except Exception as e:
            logger.error(f"Error processing dim_interation_type: {e}")
        finally:
            cursor.close()

    def process_time(self, dt_str: Optional[str]) -> Optional[int]:
        """Process and insert dim_time, returns time_id"""
        dt = self.extractor.parse_timestamp(dt_str)
        if not dt:
            return None
            
        time_id = self.extractor.calculate_time_id(dt)
        
        # Determine time slot
        hour = dt.hour
        if 5 <= hour < 12:
            slot = "Morning"
        elif 12 <= hour < 18:
            slot = "Afternoon"
        elif 18 <= hour < 22:
            slot = "Evening"
        else:
            slot = "Night"
            
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_time WHERE time_id = %s)
                INSERT INTO dim_time (time_id, [date], [week], [month], day_of_week, time_slot)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (time_id, time_id, dt.date(), dt.isocalendar()[1], dt.month, dt.strftime('%A'), slot))
        except Exception as e:
            logger.error(f"Error processing dim_time: {e}")
        finally:
            cursor.close()
            
        return time_id

    def process_context(self, statement: Statement) -> str:
        """Process dim_context and return a unique composite context_id"""
        course_id = self.extractor.extract_moodle_course_id(statement)
        resource_id = self.extractor.extract_moodle_module_id(statement.object.id)
        
        section_id = None
        learning_path_id = None
        
        # 1. Try xAPI Extensions
        if statement.context and statement.context.extensions:
            for key, val in statement.context.extensions.items():
                if 'section' in key.lower() and str(val).isdigit():
                    section_id = int(val)
                if 'path' in key.lower() and str(val).isdigit():
                    learning_path_id = int(val)

        # 2. Fallback: Moodle DB
        if resource_id and (not section_id or not learning_path_id):
            try:
                mysql_conn = self.db_manager.get_mysql_connection()
                with mysql_conn.cursor() as mysql_cursor:
                    if not section_id:
                        mysql_cursor.execute("SELECT section FROM mdl_course_modules WHERE id = %s", (resource_id,))
                        res = mysql_cursor.fetchone()
                        if res: section_id = res['section']
                    
                    if not learning_path_id:
                        mysql_cursor.execute("SELECT competencyid FROM mdl_competency_modulecomp WHERE cmid = %s", (resource_id,))
                        comp_res = mysql_cursor.fetchone()
                        if comp_res:
                            comp_id = comp_res['competencyid']
                            actor_name = statement.actor.account.name if statement.actor.account else None
                            if actor_name:
                                mysql_cursor.execute("""
                                    SELECT p.id FROM mdl_competency_plan p
                                    JOIN mdl_competency_plancomp pc ON p.id = pc.planid
                                    JOIN mdl_user u ON p.userid = u.id
                                    WHERE (u.username = %s OR u.id = %s) AND pc.competencyid = %s
                                """, (actor_name, actor_name, comp_id))
                                plan_res = mysql_cursor.fetchone()
                                if plan_res: learning_path_id = plan_res['id']
            except Exception as e:
                logger.error(f"Error fetching section/path from Moodle: {e}")

        # 3. Generate Composite context_id (e.g., CTX_12_90_273)
        c_id_part = str(course_id) if course_id else "0"
        s_id_part = str(section_id) if section_id else "0"
        r_id_part = str(resource_id) if resource_id else "0"
        context_id = f"CTX_{c_id_part}_{s_id_part}_{r_id_part}"

        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_context WHERE context_id = %s)
                INSERT INTO dim_context (context_id, course_id, section_id, learning_path_id, resource_id)
                VALUES (%s, %s, %s, %s, %s)
                ELSE
                UPDATE dim_context 
                SET course_id = %s, section_id = %s, learning_path_id = %s, resource_id = %s
                WHERE context_id = %s
            """, (context_id, context_id, course_id, section_id, learning_path_id, resource_id,
                  course_id, section_id, learning_path_id, resource_id, context_id))
        except Exception as e:
            logger.error(f"Error processing dim_context: {e}")
        finally:
            cursor.close()
            
        return context_id

    def process_activity(self, statement: Statement):
        """Process and insert/update dim_activity"""
        activity_id = statement.object.id
        activity_type = None
        content_type = None
        
        if statement.object.definition:
            activity_type = statement.object.definition.type
            # Interactivity level could be an extension
            
        cursor = self.sqlserver_conn.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_activity WHERE activity_id = %s)
                INSERT INTO dim_activity (activity_id, activity_type, content_type)
                VALUES (%s, %s, %s)
            """, (activity_id, activity_id, activity_type, content_type))
        except Exception as e:
            logger.error(f"Error processing dim_activity: {e}")
        finally:
            cursor.close()

    def process_learning_outcome(self, statement: Statement):
        """Process and insert dim_learning_outcome, fetching details from Moodle"""
        lo_ids = []
        
        # 1. Try to get from xAPI extensions
        if statement.context and statement.context.extensions:
            for key, val in statement.context.extensions.items():
                if 'outcome' in key.lower() or 'lo_' in key.lower():
                    lo_ids.append(str(val))
                    break
        
        # 2. Fallback: Try to find outcomes linked to this activity in Moodle
        if not lo_ids:
            cmid = self.extractor.extract_moodle_module_id(statement.object.id)
            if cmid:
                try:
                    mysql_conn = self.db_manager.get_mysql_connection()
                    with mysql_conn.cursor() as mysql_cursor:
                        mysql_cursor.execute("SELECT competencyid FROM mdl_competency_modulecomp WHERE cmid = %s", (cmid,))
                        results = mysql_cursor.fetchall()
                        for row in results:
                            lo_ids.append(str(row['competencyid']))
                except Exception as e:
                    logger.error(f"Error finding outcome from Moodle cmid {cmid}: {e}")

        if not lo_ids: return
        
        for lo_id in lo_ids:
            # Default values
            lo_code = lo_id
            lo_description = None
            lo_level = None
            
            # Bloom Taxonomy Mapping
            BLOOM_MAP = {
                "Remember": "Nhớ",
                "Understand": "Hiểu",
                "Apply": "Áp dụng",
                "Analyze": "Phân tích",
                "Evaluate": "Đánh giá",
                "Create": "Sáng tạo"
            }
            
            # Fetch data from Moodle
            try:
                mysql_conn = self.db_manager.get_mysql_connection()
                with mysql_conn.cursor() as mysql_cursor:
                    # Try to fetch from mdl_competency (common for Learning Outcomes in Moodle)
                    mysql_cursor.execute("""
                        SELECT shortname, idnumber, description 
                        FROM mdl_competency 
                        WHERE id = %s OR idnumber = %s
                    """, (lo_id, lo_id))
                    res = mysql_cursor.fetchone()
                    
                    if res:
                        lo_code = res['idnumber'] or res['shortname']
                        lo_description = res['description']
                        
                        # Logic to determine Bloom level from description or idnumber if keyword exists
                        content = (lo_description or "") + " " + (lo_code or "")
                        for bloom_en, bloom_vi in BLOOM_MAP.items():
                            if bloom_en.lower() in content.lower():
                                lo_level = bloom_vi
                                break
            except Exception as e:
                logger.error(f"Error fetching outcome details from Moodle: {e}")

            # Save to SQL Server
            cursor = self.sqlserver_conn.cursor()
            try:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM dim_learning_outcome WHERE outcome_id = %s)
                    INSERT INTO dim_learning_outcome (outcome_id, outcome_code, outcome_description, outcome_level)
                    VALUES (%s, %s, %s, %s)
                    ELSE
                    UPDATE dim_learning_outcome 
                    SET outcome_code = %s, outcome_description = %s, outcome_level = %s
                    WHERE outcome_id = %s
                """, (lo_id, lo_id, lo_code, lo_description, lo_level, lo_code, lo_description, lo_level, lo_id))
            except Exception as e:
                logger.error(f"Error processing dim_learning_outcome: {e}")
            finally:
                cursor.close()

    def process_all(self, statement: Statement) -> str:
        """Process all dimensions for a statement and return context_id"""
        self.process_actor(statement)
        self.process_interaction_type(statement)
        self.process_time(statement.timestamp)
        context_id = self.process_context(statement)
        self.process_activity(statement)
        self.process_learning_outcome(statement)
        return context_id
