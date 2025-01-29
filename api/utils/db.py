from pymongo import MongoClient
from functools import lru_cache
from dotenv import load_dotenv
import os
import logging
import certifi

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@lru_cache()
def get_db():
    """
    Create and return a cached database connection.
    Uses LRU cache to prevent creating multiple instances.
    """
    try:
        # Use certifi for SSL certificate verification
        client = MongoClient(
            os.getenv('MONGODB_URI'),
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000  # 5 second timeout
        )
        
        # Test the connection
        client.server_info()
        logger.info("Successfully connected to MongoDB")
        
        # Get database name from connection string or use default
        db_name = os.getenv('DB_NAME', 'movies_database')
        return client[db_name]
    
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

# Initialize database connection
try:
    db = get_db()
except Exception as e:
    logger.error(f"Database initialization failed: {str(e)}")
    db = None
