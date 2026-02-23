import logging
from typing import List, Dict, Any
from etl_app.database.connection import DatabaseManager
from etl_app.models.xapi_models import Statement
from etl_app.etl.dimension_processor import DimensionProcessor
from etl_app.etl.fact_processor import FactProcessor
from etl_app.etl.bridge_processor import BridgeProcessor
from etl_app.etl.utils import DataExtractor

logger = logging.getLogger(__name__)


class ETLManager:
    """Coordinates the ETL process for the new schema"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.sqlserver_conn = self.db_manager.get_sqlserver_connection()
        
        self.dim_processor = DimensionProcessor(self.db_manager)
        self.fact_processor = FactProcessor(self.db_manager)
        self.bridge_processor = BridgeProcessor(self.db_manager) # Added
        self.extractor = DataExtractor()
        
    def run(self, statements: List[Dict[str, Any]]):
        """Run the ETL process for a batch of statements"""
        # Sort statements by timestamp ASCENDING to ensure chronological processing
        # This is critical for session start/end and state-based logic
        statements.sort(key=lambda x: x.get('timestamp', ''))
        
        logger.info(f"Starting ETL for {len(statements)} statements")
        processed_count = 0
        
        for stmt_data in statements:
            try:
                statement = Statement(**stmt_data)
                
                # 1. Process Dimensions
                context_id = self.dim_processor.process_all(statement)
                
                # 2. Extract time_id
                dt = self.extractor.parse_timestamp(statement.timestamp)
                time_id = self.extractor.calculate_time_id(dt) if dt else 0
                
                # 3. Process Facts
                self.fact_processor.process_all(statement, time_id, context_id)
                
                # 4. Process Bridge (Hierarchy)
                self.bridge_processor.process_activity_hierarchy(statement) # Added
                
                processed_count += 1
                if processed_count % 100 == 0:
                    logger.info(f"Processed {processed_count}/{len(statements)} statements...")
                
            except Exception as e:
                logger.error(f"Error processing statement {stmt_data.get('id')}: {e}")
                continue
                
        # Commit transaction
        try:
            self.sqlserver_conn.commit()
            logger.info(f"ETL batch committed successfully. Processed {processed_count}/{len(statements)} statements.")
            print(f"ETL Success: {processed_count} new/updated records processed.")
        except Exception as e:
            self.sqlserver_conn.rollback()
            logger.error(f"Transaction failed, rolled back: {e}")
            
    def close(self):
        self.db_manager.close_all()
