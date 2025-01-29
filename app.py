from api import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode
    app.run(host='0.0.0.0', port=8000, debug=True) 