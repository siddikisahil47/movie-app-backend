from pymongo import MongoClient
from functools import lru_cache
from config import Config
import ssl

@lru_cache()
def get_mongodb_client():
    """
    Create and return a cached MongoDB client instance.
    Uses LRU cache to prevent creating multiple instances.
    """
    try:
        client = MongoClient(
            Config.MONGODB_URI,
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        return client
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

def get_db():
    """
    Get database connection.
    Returns the MongoDB database instance for operations.
    """
    client = get_mongodb_client()
    db = client['movies_database']
    return db
