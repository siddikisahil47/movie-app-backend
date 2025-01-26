from flask import Blueprint, jsonify, request
from api.models.movie import Movie, MovieDetail
from typing import Dict, Any

movies = Blueprint('movies', __name__)

@movies.route('/api/v1/movies', methods=['POST'])
async def create_movie():
    """Create a new movie with details."""
    try:
        data: Dict[str, Any] = request.get_json()
        
        # Split data into movie and details
        movie_data = {
            'movie_id': data.get('movie_id'),
            'title': data.get('title'),
            'year': data.get('year'),
            'runtime': data.get('runtime'),
            'image_url': data.get('image_url'),
            'poster_url': data.get('poster_url')
        }
        
        movie_details = {
            'title': data.get('title'),
            'year': data.get('year'),
            'ua': data.get('ua'),
            'match': data.get('match'),
            'runtime': data.get('runtime'),
            'hdsd': data.get('hdsd'),
            'type': data.get('type'),
            'director': data.get('director'),
            'writer': data.get('writer'),
            'producers': data.get('producers'),
            'studio': data.get('studio'),
            'cast_members': data.get('cast_members'),
            'genre': data.get('genre'),
            'description': data.get('description'),
            'languages': data.get('languages'),
            'image_url': data.get('image_url'),
            'poster_url': data.get('poster_url')
        }
        
        result = await MovieDetail.create_with_movie(movie_data, movie_details)
        return jsonify(result), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/api/v1/movies/<movie_id>', methods=['GET'])
async def get_movie(movie_id: str):
    """Get a movie by its ID with full details."""
    try:
        movie = await MovieDetail.get_full_movie(movie_id)
        if not movie:
            return jsonify({'error': 'Movie not found'}), 404
        return jsonify(movie), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/api/v1/movies', methods=['GET'])
async def search_movies():
    """Search movies by title."""
    try:
        title = request.args.get('title', '')
        if not title:
            return jsonify({'error': 'Title parameter is required'}), 400
            
        movies = await Movie.search_by_title(title)
        return jsonify(movies), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/api/v1/movies/latest', methods=['GET'])
async def get_latest_movies():
    """Get latest movies."""
    try:
        # Using raw SQL for ordering by created_at
        response = Movie.get_db().table('movies')\
            .select('*')\
            .order('created_at', desc=True)\
            .limit(10)\
            .execute()
            
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/api/v1/genres', methods=['GET'])
async def get_genres():
    """Get all unique genres."""
    try:
        genres = await MovieDetail.get_all_genres()
        # print("Fetched genres:", genres)  # Debug print
        return jsonify(genres), 200
    except Exception as e:
        print(f"Error in get_genres: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@movies.route('/api/v1/movies/genre/<genre>', methods=['GET'])
async def get_movies_by_genre(genre: str):
    """Get movies by genre."""
    try:
        response = MovieDetail.get_db().table('movie_details')\
            .select('*, movies!inner(*)')\
            .ilike('genre', f'%{genre}%')\
            .execute()
            
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/api/v1/movies/random', methods=['GET'])
async def get_random_movies():
    """Get random movies."""
    try:
        # Using raw SQL for random selection
        response = Movie.get_db().table('movies')\
            .select('*')\
            .limit(10)\
            .execute()
            
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/api/v1/movies/featured', methods=['GET'])
async def get_featured_movies():
    """Get featured movies."""
    try:
        # Get limit from query parameters, default to 10
        limit = request.args.get('limit', default=10, type=int)
        
        # Ensure limit is within reasonable bounds
        limit = max(1, min(limit, 20))  # Between 1 and 20
        
        featured_movies = await MovieDetail.get_featured_movies(limit)
        return jsonify(featured_movies), 200
    except Exception as e:
        print(f"Error in get_featured_movies: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500