import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # API settings
    API_TITLE = 'Movie App API'
    API_VERSION = 'v1'
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://"
