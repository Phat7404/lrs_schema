import logging
import sys
from etl_app.etl.manager import ETLManager

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def run_etl():
    """Main ETL loop: Fetch from LRS -> Process -> Save to SQL Server"""
    print("ETL App Initialized. Starting data processing...")
    
    from etl_app.services.xapi_service import XAPIService
    
    xapi_service = XAPIService()
    etl_manager = ETLManager()
    
    try:
        # Fetch a batch of statements (defaulting to 100 for now)
        print("Fetching statements from xAPI LRS...")
        statements = xapi_service.fetch_statements(limit=500)
        
        if not statements:
            print("No new statements found.")
            return

        print(f"Starting processing of {len(statements)} statements.")
        etl_manager.run(statements)
        print("ETL Process completed successfully.")
        
    except Exception as e:
        logging.error(f"ETL Execution failed: {e}", exc_info=True)
    finally:
        etl_manager.close()

if __name__ == "__main__":
    run_etl()
