from flask import Blueprint, jsonify, request
from api.models.movie import Movie, MovieDetail
from typing import Dict, Any
from bson import ObjectId
from datetime import datetime
import uuid
from api.utils.db import get_db

movies = Blueprint('movies', __name__)

def generate_movie_id():
    """Generate a unique movie ID"""
    return uuid.uuid4().hex.upper()[:26]

@movies.route('/movies', methods=['POST'])
def create_movie():
    """Create a new movie"""
    try:
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400

        movie = {
            'movie_id': generate_movie_id(),
            'title': data['title'],
            'year': data.get('year'),
            'runtime': data.get('runtime'),
            'created_at': datetime.utcnow(),
            'streaming_platforms': []
        }

        # Add streaming platforms if provided
        if data.get('streaming_platforms'):
            for platform in data['streaming_platforms']:
                platform_doc = {
                    'platform_id': ObjectId(platform['platform_id']),
                    'platform_name': platform['platform_name'],
                    'available_until': datetime.fromisoformat(platform['available_until'].replace('Z', '+00:00')),
                    'added_date': datetime.fromisoformat(platform['added_date'].replace('Z', '+00:00'))
                }
                movie['streaming_platforms'].append(platform_doc)
        
        db = get_db()
        result = db.movies.insert_one(movie)
        
        # Convert ObjectId to string for response
        movie['_id'] = str(result.inserted_id)
        for platform in movie['streaming_platforms']:
            platform['platform_id'] = str(platform['platform_id'])
            platform['available_until'] = platform['available_until'].isoformat()
            platform['added_date'] = platform['added_date'].isoformat()
        
        return jsonify(movie), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/movies', methods=['GET'])
def get_movies():
    """Get all movies"""
    try:
        db = get_db()
        movies_list = list(db.movies.find())
        
        # Convert ObjectId and dates to string for JSON serialization
        for movie in movies_list:
            movie['_id'] = str(movie['_id'])
            if movie.get('streaming_platforms'):
                for platform in movie['streaming_platforms']:
                    if platform.get('platform_id'):
                        platform['platform_id'] = str(platform['platform_id'])
                    if platform.get('available_until'):
                        platform['available_until'] = platform['available_until'].isoformat()
                    if platform.get('added_date'):
                        platform['added_date'] = platform['added_date'].isoformat()
            
        return jsonify(movies_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get a specific movie"""
    try:
        db = get_db()
        movie = db.movies.find_one({'movie_id': movie_id})
        
        if not movie:
            return jsonify({'error': 'Movie not found'}), 404
            
        # Convert ObjectId and dates to string for JSON serialization
        movie['_id'] = str(movie['_id'])
        if movie.get('streaming_platforms'):
            for platform in movie['streaming_platforms']:
                if platform.get('platform_id'):
                    platform['platform_id'] = str(platform['platform_id'])
                if platform.get('available_until'):
                    platform['available_until'] = platform['available_until'].isoformat()
                if platform.get('added_date'):
                    platform['added_date'] = platform['added_date'].isoformat()
        
        return jsonify(movie), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/movies/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """Update a movie"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        db = get_db()
        update_data = {}
        
        # Update basic fields if provided
        if 'title' in data:
            update_data['title'] = data['title']
        if 'year' in data:
            update_data['year'] = data['year']
        if 'runtime' in data:
            update_data['runtime'] = data['runtime']
            
        # Update streaming platforms if provided
        if 'streaming_platforms' in data:
            platforms = []
            for platform in data['streaming_platforms']:
                platform_doc = {
                    'platform_id': ObjectId(platform['platform_id']),
                    'platform_name': platform['platform_name'],
                    'available_until': datetime.fromisoformat(platform['available_until'].replace('Z', '+00:00')),
                    'added_date': datetime.fromisoformat(platform['added_date'].replace('Z', '+00:00'))
                }
                platforms.append(platform_doc)
            update_data['streaming_platforms'] = platforms
        
        result = db.movies.update_one(
            {'movie_id': movie_id},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Movie not found'}), 404
            
        return jsonify({'message': 'Movie updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    """Delete a movie"""
    try:
        db = get_db()
        result = db.movies.delete_one({'movie_id': movie_id})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Movie not found'}), 404
            
        return jsonify({'message': 'Movie deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies.route('/movies/search', methods=['GET'])
def search_movies():
    """Search movies by title"""
    try:
        title = request.args.get('title', '')
        if not title:
            return jsonify({'error': 'Title parameter is required'}), 400

        db = get_db()
        movies_list = list(db.movies.find(
            {'title': {'$regex': title, '$options': 'i'}}
        ))

        # Convert ObjectId and dates to string for JSON serialization
        for movie in movies_list:
            movie['_id'] = str(movie['_id'])
            if movie.get('streaming_platforms'):
                for platform in movie['streaming_platforms']:
                    if platform.get('platform_id'):
                        platform['platform_id'] = str(platform['platform_id'])
                    if platform.get('available_until'):
                        platform['available_until'] = platform['available_until'].isoformat()
                    if platform.get('added_date'):
                        platform['added_date'] = platform['added_date'].isoformat()
            
        return jsonify(movies_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
