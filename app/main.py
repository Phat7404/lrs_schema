from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging
from typing import List, Dict, Any
from app.config import settings
from app.database.connection import DatabaseManager
from app.services.xapi_service import XAPIService
from app.etl.processor import ETLProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="xAPI Data Warehouse ETL Service", version="1.0.0")

# Global instances
db_manager = DatabaseManager()
xapi_service = XAPIService()


@app.on_event("startup")
async def startup_event():
    """Initialize service on startup (lazy database connections)"""
    logger.info("Service starting up...")
    logger.info("Database connections will be established on first use")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    logger.info("Closing database connections...")
    db_manager.close_all()
    logger.info("Database connections closed")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "xAPI Data Warehouse ETL Service",
        "version": "1.0.0",
        "endpoints": {
            "/fetch-and-load": "Fetch xAPI statements and load into data warehouse",
            "/fetch-and-load-batch": "Fetch xAPI statements with pagination",
            "/health": "Health check endpoint"
        }
    }


@app.get("/test-xapi")
async def test_xapi():
    """Test xAPI LRS connection and return detailed response"""
    try:
        test_result = xapi_service.test_connection()
        return test_result
    except Exception as e:
        logger.error(f"Error testing xAPI connection: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "service": "running"
    }
    
    # Check SQL Server connection (optional)
    try:
        sqlserver_conn = db_manager.get_sqlserver_connection()
        sqlserver_cursor = sqlserver_conn.cursor()
        sqlserver_cursor.execute("SELECT 1")
        sqlserver_cursor.close()
        health_status["sqlserver"] = "connected"
    except Exception as e:
        logger.warning(f"SQL Server connection check failed: {e}")
        health_status["sqlserver"] = f"disconnected: {str(e)[:100]}"
        health_status["status"] = "degraded"
    
    # Check MySQL connection (optional)
    try:
        mysql_conn = db_manager.get_mysql_connection()
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute("SELECT 1")
        mysql_cursor.close()
        health_status["mysql"] = "connected"
    except Exception as e:
        logger.warning(f"MySQL connection check failed: {e}")
        health_status["mysql"] = f"disconnected: {str(e)[:100]}"
        health_status["status"] = "degraded"
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return JSONResponse(status_code=status_code, content=health_status)


@app.post("/fetch-and-load")
async def fetch_and_load():
    """
    Main endpoint: Fetch xAPI statements from LRS and load into data warehouse
    
    This endpoint:
    1. Fetches statements from the xAPI LRS
    2. Processes each statement through ETL pipeline
    3. Loads data into dimension and fact tables
    4. Returns summary of processed statements
    """
    try:
        logger.info("Starting fetch-and-load process...")
        
        # Step 1: Fetch statements from xAPI LRS
        statements = xapi_service.fetch_statements()
        
        if not statements:
            return {
                "status": "success",
                "message": "No statements found",
                "processed_count": 0
            }
        
        # Step 2: Process statements through ETL
        etl_processor = ETLProcessor(db_manager)
        etl_processor.process_statements(statements)
        
        logger.info(f"Successfully processed {len(statements)} statements")
        
        return {
            "status": "success",
            "message": f"Successfully processed {len(statements)} statements",
            "processed_count": len(statements)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in fetch-and-load: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing statements: {str(e)}")


@app.post("/fetch-and-load-batch")
async def fetch_and_load_batch(limit: int = 100, offset: int = 0):
    """
    Fetch xAPI statements with pagination and load into data warehouse
    
    Parameters:
    - limit: Maximum number of statements to fetch (default: 100)
    - offset: Number of statements to skip (default: 0)
    """
    try:
        logger.info(f"Starting batch fetch-and-load process (limit={limit}, offset={offset})...")
        
        # Fetch statements with pagination
        statements = xapi_service.fetch_statements(limit=limit, offset=offset)
        
        if not statements:
            return {
                "status": "success",
                "message": "No statements found in this batch",
                "processed_count": 0,
                "limit": limit,
                "offset": offset
            }
        
        # Process statements through ETL
        etl_processor = ETLProcessor(db_manager)
        etl_processor.process_statements(statements)
        
        logger.info(f"Successfully processed {len(statements)} statements in batch")
        
        return {
            "status": "success",
            "message": f"Successfully processed {len(statements)} statements",
            "processed_count": len(statements),
            "limit": limit,
            "offset": offset
        }
    
    except Exception as e:
        logger.error(f"Error in fetch-and-load-batch: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing statements: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

