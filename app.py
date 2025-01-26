from api import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode
    app.run(
        host='0.0.0.0',  # Listen on all available interfaces
        port=5001,       # Port 5000 is Flask's default
        debug=True       # Enable debug mode for development
    ) 