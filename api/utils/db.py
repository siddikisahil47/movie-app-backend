from pymongo import MongoClient
from functools import lru_cache
from dotenv import load_dotenv
import os
import logging
import certifi
import dns.resolver

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
        mongodb_uri = os.getenv('MONGODB_URI')
        logger.info(f"Attempting to connect to MongoDB...")
        
        # Use certifi for SSL certificate verification
        client = MongoClient(
            mongodb_uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=10000,
            retryWrites=True,
            w='majority'
        )
        
        # Test the connection
        client.server_info()
        logger.info("Successfully connected to MongoDB")
        
        # Get database name from connection string or use default
        db_name = os.getenv('DB_NAME', 'movies_database')
        return client[db_name]
    
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        # Log more details about the connection attempt
        logger.error(f"Connection URI (masked): {mongodb_uri.split('@')[0]}@{'@'.join(mongodb_uri.split('@')[1:])}")
        raise

# Initialize database connection
try:
    db = get_db()
except Exception as e:
    logger.error(f"Database initialization failed: {str(e)}")
    db = None
