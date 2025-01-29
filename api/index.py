from flask import Flask
from api import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()

# For Vercel serverless deployment
if __name__ == '__main__':
    app.run() 