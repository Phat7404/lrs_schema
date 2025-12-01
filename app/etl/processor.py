import logging
import uuid
from typing import List, Dict, Any
from app.models.xapi_models import Statement
from app.database.connection import DatabaseManager
from app.etl.dimension_processor import DimensionProcessor
from app.etl.fact_processor import FactProcessor
from app.etl.bridge_processor import BridgeProcessor
from app.etl.utils import DataExtractor

logger = logging.getLogger(__name__)


class ETLProcessor:
    """Main ETL processor that coordinates all processing"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.sqlserver_conn = db_manager.get_sqlserver_connection()
        
        # Initialize processors
        self.dimension_processor = DimensionProcessor(db_manager)
        self.fact_processor = FactProcessor(db_manager)
        self.bridge_processor = BridgeProcessor(db_manager)
        self.extractor = DataExtractor()
    
    def process_statements(self, statements: List[Dict[str, Any]]):
        """
        Process a list of xAPI statements and load into data warehouse
        
        Args:
            statements: List of statement dictionaries from xAPI LRS
        """
        logger.info(f"Processing {len(statements)} statements")
        
        for stmt_data in statements:
            try:
                statement = Statement(**stmt_data)
                self.process_statement(statement)
            except Exception as e:
                logger.error(f"Error processing statement: {e}", exc_info=True)
                continue
        
        # Commit all changes
        try:
            self.sqlserver_conn.commit()
            logger.info("All statements processed and committed")
        except Exception as e:
            logger.error(f"Error committing transaction: {e}")
            self.sqlserver_conn.rollback()
            raise
    
    def process_statement(self, statement: Statement):
        """
        Process a single xAPI statement
        
        Args:
            statement: Statement object
        """
        # Extract statement ID and convert to UUID format
        stmt_id = statement.id
        if not stmt_id:
            stmt_id = str(uuid.uuid4())
        else:
            stmt_id = self.extractor.normalize_uuid(stmt_id)
        
        # Process dimensions first (they must exist before facts)
        self.dimension_processor.process_all_dimensions(statement)
        
        # Process fact_statement
        self.fact_processor.process_statement(statement, stmt_id)
        
        # Process specialized facts based on verb
        verb_id = statement.verb.id.lower()
        if 'quiz' in verb_id or 'completed' in verb_id:
            self.fact_processor.process_quiz(statement, stmt_id)
        
        if 'answered' in verb_id:
            self.fact_processor.process_question_answer(statement, stmt_id)
        
        # Process bridge table (Activity Hierarchy)
        self.bridge_processor.process_activity_hierarchy(statement)

