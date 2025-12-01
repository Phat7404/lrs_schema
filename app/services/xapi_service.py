import requests
import base64
import logging
from typing import List, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)


class XAPIService:
    """Service for fetching xAPI statements from LRS"""
    
    def __init__(self):
        self.url = settings.xapi_url
        self.username = settings.xapi_username
        self.password = settings.xapi_password
    
    def _get_auth_header(self) -> str:
        """Create Basic Auth header"""
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to xAPI LRS
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            headers = {
                "Authorization": self._get_auth_header(),
                "Accept": "application/json",
                "X-Experience-API-Version": "1.0.3"
            }
            
            # Try a simple GET request with minimal parameters
            logger.info(f"Testing connection to {self.url}")
            response = requests.get(self.url, headers=headers, params={"limit": 1}, timeout=10)
            
            return {
                "status": "success" if response.status_code == 200 else "error",
                "status_code": response.status_code,
                "url": self.url,
                "headers_sent": {k: "***" if k == "Authorization" else v for k, v in headers.items()},
                "response_headers": dict(response.headers),
                "response_preview": response.text[:200] if response.text else "No response body"
            }
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "url": self.url
            }
    
    def fetch_statements(self, limit: int = None, offset: int = None) -> List[Dict[str, Any]]:
        """
        Fetch xAPI statements from LRS
        
        Args:
            limit: Maximum number of statements to fetch
            offset: Number of statements to skip
            
        Returns:
            List of statement dictionaries
        """
        try:
            headers = {
                "Authorization": self._get_auth_header(),
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Experience-API-Version": "1.0.3"
            }
            
            params = {}
            if limit is not None:
                params["limit"] = limit
            if offset is not None:
                params["offset"] = offset
            
            logger.info(f"Fetching statements from {self.url} with params: {params}")
            response = requests.get(self.url, headers=headers, params=params, timeout=30)
            
            # Log response details for debugging
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
            
            # Check for error response
            if response.status_code != 200:
                error_detail = f"Status {response.status_code}"
                try:
                    error_body = response.text[:500]  # First 500 chars
                    logger.error(f"Error response body: {error_body}")
                    error_detail += f" - {error_body}"
                except:
                    pass
                response.raise_for_status()
            
            # Try to parse JSON response
            try:
                data = response.json()
            except ValueError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Response text: {response.text[:500]}")
                raise ValueError(f"Invalid JSON response from xAPI LRS: {e}")
            
            # xAPI can return either a single statement or an array
            # Also handle the case where response is wrapped in a "statements" key
            if isinstance(data, dict):
                # Check if it's a paginated response with "statements" key
                if "statements" in data and isinstance(data["statements"], list):
                    statements = data["statements"]
                # Check if it's a single statement object
                elif "id" in data or "actor" in data:
                    statements = [data]
                else:
                    logger.warning(f"Unexpected response format: {data.keys()}")
                    statements = []
            elif isinstance(data, list):
                statements = data
            else:
                logger.warning(f"Unexpected response type: {type(data)}")
                statements = []
            
            logger.info(f"Fetched {len(statements)} statements")
            return statements
        
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error fetching xAPI statements: {e}"
            if hasattr(e.response, 'text'):
                error_msg += f" - Response: {e.response.text[:500]}"
            logger.error(error_msg)
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching xAPI statements: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching statements: {e}", exc_info=True)
            raise

