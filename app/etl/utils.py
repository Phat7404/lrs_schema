import re
import uuid
import logging
from typing import Optional
from datetime import datetime
from app.models.xapi_models import Statement

logger = logging.getLogger(__name__)


class DataExtractor:
    """Utility class for extracting and parsing data from xAPI statements"""
    
    @staticmethod
    def extract_moodle_module_id(url: str) -> Optional[int]:
        """Extract Moodle module ID (cmid) from URL"""
        if not url:
            return None
        
        # Try to find cmid=X pattern
        match = re.search(r'cmid[=:](\d+)', url, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # Try to find id=X pattern
        match = re.search(r'[?&]id=(\d+)', url)
        if match:
            return int(match.group(1))
        
        return None
    
    @staticmethod
    def extract_moodle_course_id(statement: Statement) -> Optional[int]:
        """Extract Moodle course ID from contextActivities"""
        if not statement.context or not statement.context.contextActivities:
            return None
        
        if statement.context.contextActivities.parent:
            for parent in statement.context.contextActivities.parent:
                if 'course' in parent.id.lower():
                    match = re.search(r'id=(\d+)', parent.id)
                    if match:
                        return int(match.group(1))
        
        return None
    
    @staticmethod
    def parse_timestamp(timestamp_str: Optional[str]) -> Optional[datetime]:
        """Parse ISO 8601 timestamp string to datetime"""
        if not timestamp_str:
            return None
        
        try:
            # Remove timezone info if present for SQL Server compatibility
            timestamp_str = timestamp_str.replace('Z', '+00:00')
            if '+' in timestamp_str or timestamp_str.count('-') > 2:
                # Has timezone
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            else:
                # No timezone
                dt = datetime.fromisoformat(timestamp_str)
            return dt
        except Exception as e:
            logger.error(f"Error parsing timestamp {timestamp_str}: {e}")
            return None
    
    @staticmethod
    def parse_duration(duration_str: Optional[str]) -> Optional[int]:
        """Parse ISO 8601 duration to seconds"""
        if not duration_str:
            return None
        
        try:
            # Simple parser for PT1H2M3S format
            total_seconds = 0
            duration_str = duration_str.replace('PT', '')
            
            # Extract hours
            hours_match = re.search(r'(\d+)H', duration_str)
            if hours_match:
                total_seconds += int(hours_match.group(1)) * 3600
            
            # Extract minutes
            minutes_match = re.search(r'(\d+)M', duration_str)
            if minutes_match:
                total_seconds += int(minutes_match.group(1)) * 60
            
            # Extract seconds
            seconds_match = re.search(r'(\d+)S', duration_str)
            if seconds_match:
                total_seconds += int(seconds_match.group(1))
            
            return total_seconds if total_seconds > 0 else None
        except Exception as e:
            logger.error(f"Error parsing duration {duration_str}: {e}")
            return None
    
    @staticmethod
    def normalize_uuid(uuid_str: Optional[str]) -> Optional[str]:
        """Normalize UUID string to valid UUID format"""
        if not uuid_str:
            return None
        
        try:
            uuid.UUID(uuid_str)
            return uuid_str
        except ValueError:
            # If not valid UUID, generate one from hash
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, uuid_str))
    
    @staticmethod
    def extract_event_name(statement: Statement) -> Optional[str]:
        """Extract event_name from statement context extensions"""
        if not statement.context or not statement.context.extensions:
            return None
        
        for key, value in statement.context.extensions.items():
            if 'event_name' in key.lower() or 'info' in key.lower():
                if isinstance(value, dict) and 'event_name' in value:
                    return value['event_name']
                elif isinstance(value, str):
                    return value
        
        return None

