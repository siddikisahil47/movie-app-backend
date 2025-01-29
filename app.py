from flask import Flask
from api import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) 