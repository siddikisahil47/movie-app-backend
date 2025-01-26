from supabase import create_client
from functools import lru_cache
from config import Config

@lru_cache()
def get_supabase_client():
    """
    Create and return a cached Supabase client instance.
    Uses LRU cache to prevent creating multiple instances.
    """
    try:
        client = create_client(
            supabase_url=Config.SUPABASE_URL,
            supabase_key=Config.SUPABASE_KEY
        )
        return client
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Supabase: {str(e)}")

def get_db():
    """
    Get database connection.
    Returns the Supabase client for database operations.
    """
    return get_supabase_client()
