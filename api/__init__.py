from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from api.routes.movies import movies
    app.register_blueprint(movies)
    
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy'}, 200
    
    return app