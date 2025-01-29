import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_config():
    return {
        'MONGODB_URI': os.getenv('MONGODB_URI'),
        'DB_NAME': os.getenv('DB_NAME', 'movies_database')
    }

class Config:
    """Application configuration class."""
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'movies_database')
    if MONGODB_URI and 'mongodb+srv://' in MONGODB_URI:
        MONGODB_URI += '?tls=true'
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # API Configuration
    API_TITLE = 'Movie App API'
    API_VERSION = 'v1'
    
    # Flask settings
    # FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    # DEBUG = FLASK_ENV == 'development'
    
    # API settings
    API_TITLE = 'Movie App API'
    API_VERSION = 'v1'
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://"
