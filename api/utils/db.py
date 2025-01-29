from pymongo import MongoClient
from functools import lru_cache
# from config import Config
from ssl import CERT_NONE
from dotenv import load_dotenv
import os

load_dotenv()

@lru_cache()
def get_mongodb_client():
    """
    Create and return a cached MongoDB client instance.
    Uses LRU cache to prevent creating multiple instances.
    """
    try:
        client = MongoClient(
            os.getenv("MONGODB_URI"),
            ssl=True,
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000
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
