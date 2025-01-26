from api.utils.db import get_db
from typing import Dict, List, Optional, Any

class BaseModel:
    """Base model class with common database operations."""
    
    table_name: str = None
    
    @classmethod
    def get_db(cls):
        return get_db()
    
    @classmethod
    async def find_by_id(cls, id: str) -> Optional[Dict]:
        """Retrieve a record by ID."""
        try:
            response = cls.get_db().table(cls.table_name).select("*").eq("id", id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error retrieving {cls.table_name}: {str(e)}")
    
    @classmethod
    async def find_all(cls) -> List[Dict]:
        """Retrieve all records."""
        try:
            response = cls.get_db().table(cls.table_name).select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error retrieving {cls.table_name}s: {str(e)}")
    
    @classmethod
    async def create(cls, data: Dict[str, Any]) -> Dict:
        """Create a new record."""
        try:
            response = cls.get_db().table(cls.table_name).insert(data).execute()
            return response.data[0]
        except Exception as e:
            raise Exception(f"Error creating {cls.table_name}: {str(e)}")
    
    @classmethod
    async def update(cls, id: str, data: Dict[str, Any]) -> Optional[Dict]:
        """Update a record by ID."""
        try:
            response = cls.get_db().table(cls.table_name).update(data).eq("id", id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error updating {cls.table_name}: {str(e)}")
    
    @classmethod
    async def delete(cls, id: str) -> bool:
        """Delete a record by ID."""
        try:
            response = cls.get_db().table(cls.table_name).delete().eq("id", id).execute()
            return bool(response.data)
        except Exception as e:
            raise Exception(f"Error deleting {cls.table_name}: {str(e)}")
