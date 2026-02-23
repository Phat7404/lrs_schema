import requests
import base64
import logging
from typing import List, Dict, Any
from etl_app.config import settings

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
    
    def fetch_statements(self, limit: int = None) -> List[Dict[str, Any]]:
        """Fetch xAPI statements from LRS, handling pagination if more data is available"""
        try:
            all_statements = []
            headers = {
                "Authorization": self._get_auth_header(),
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Experience-API-Version": "1.0.3"
            }
            
            # First request
            params = {}
            if limit is not None:
                params["limit"] = limit
            
            current_url = self.url
            
            while True:
                logger.info(f"Fetching from: {current_url}")
                # For pagination, we use the full URL provided by 'more', which includes auth sometimes but headers are safer
                response = requests.get(current_url, headers=headers, params=params if current_url == self.url else None, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                batch = []
                more_url = None
                
                if isinstance(data, dict):
                    batch = data.get("statements", [])
                    more_url = data.get("more")
                elif isinstance(data, list):
                    batch = data
                
                all_statements.extend(batch)
                logger.info(f"Fetched {len(batch)} statements. Total: {len(all_statements)}")

                # Check if we have enough or if there are no more pages
                if not more_url or (limit and len(all_statements) >= limit):
                    break
                
                # Update URL for next iteration
                # Note: 'more' usually comes as a relative URL from the LRS root or a full URL
                if more_url.startswith("http"):
                    current_url = more_url
                else:
                    # Construct full URL if relative
                    from urllib.parse import urljoin
                    current_url = urljoin(self.url, more_url)
                
            # Truncate if we exceeded limit during the last batch
            if limit and len(all_statements) > limit:
                all_statements = all_statements[:limit]

            if all_statements:
                first_stmt = all_statements[0]
                actor = first_stmt.get("actor", {}).get("account", {}).get("name") or first_stmt.get("actor", {}).get("name", "Unknown")
                verb = first_stmt.get("verb", {}).get("display", {}).get("en") or first_stmt.get("verb", {}).get("id")
                logger.info(f"Summary - Total: {len(all_statements)}, Last Actor: {actor}, Last Verb: {verb}")
                
            return all_statements
        except Exception as e:
            logger.error(f"Error fetching xAPI statements: {e}")
            raise
