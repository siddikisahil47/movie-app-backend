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
    from api.routes.streaming import streaming
    from api.routes.genres import genres
    from api.routes.movie_details import movie_details
    
    app.register_blueprint(movies, url_prefix='/api/v1')
    app.register_blueprint(streaming, url_prefix='/api/v1')
    app.register_blueprint(genres, url_prefix='/api/v1')
    app.register_blueprint(movie_details, url_prefix='/api/v1')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy'}, 200
    
    @app.route('/')
    def home():
        return {'status': 'API is running'}
    
    return app