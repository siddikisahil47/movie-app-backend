from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
import uuid
from api.utils.db import get_db

movie_details = Blueprint('movie_details', __name__)

def generate_movie_id():
    """Generate a unique movie ID"""
    return uuid.uuid4().hex.upper()[:26]

@movie_details.route('/movies/complete', methods=['POST'])
def create_complete_movie():
    """Create a complete movie with details, genres, and streaming platforms"""
    try:
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400

        db = get_db()
        movie_id = generate_movie_id()
        current_time = datetime.utcnow()

        # 1. Create base movie record
        movie = {
            'movie_id': movie_id,
            'title': data['title'],
            'year': data.get('year'),
            'runtime': data.get('runtime'),
            'created_at': current_time,
            'streaming_platforms': []
        }

        # 2. Create movie details
        movie_detail = {
            'movie_id': movie_id,
            'title': data['title'],
            'year': data.get('year'),
            'ua': data.get('ua'),
            'rating': data.get('rating'),
            'is_featured': data.get('is_featured', False),
            'is_latest': data.get('is_latest', False),
            'runtime': data.get('runtime'),
            'description': data.get('description'),
            'director': data.get('director'),
            'writers': data.get('writers', []),
            'studio': data.get('studio'),
            'cast_members': data.get('cast_members', []),
            'created_at': current_time,
            'genres': [],
            'streaming_platforms': []
        }

        # 3. Process genres
        if data.get('genres'):
            for genre_data in data['genres']:
                # Check if genre exists
                genre = db.genres.find_one({'name': genre_data['name']})
                if not genre:
                    # Create new genre if it doesn't exist
                    genre_result = db.genres.insert_one({
                        'name': genre_data['name'],
                        'created_at': current_time
                    })
                    genre_id = genre_result.inserted_id
                else:
                    genre_id = genre['_id']

                # Add to movie details
                genre_doc = {
                    'id': genre_id,
                    'name': genre_data['name']
                }
                movie_detail['genres'].append(genre_doc)

        # 4. Process streaming platforms
        if data.get('streaming_platforms'):
            for platform_data in data['streaming_platforms']:
                # Check if platform exists
                platform = db.streaming_platforms_list.find_one({'name': platform_data['platform_name']})
                if not platform:
                    # Create new platform if it doesn't exist
                    platform_result = db.streaming_platforms_list.insert_one({
                        'name': platform_data['platform_name'],
                        'active': True,
                        'created_at': current_time
                    })
                    platform_id = platform_result.inserted_id
                else:
                    platform_id = platform['_id']

                # Create platform document for both movie and movie_detail
                platform_doc = {
                    'platform_id': platform_id,
                    'platform_name': platform_data['platform_name'],
                    'available_until': datetime.fromisoformat(platform_data['available_until'].replace('Z', '+00:00')) if platform_data.get('available_until') else None,
                    'added_date': current_time
                }
                movie['streaming_platforms'].append(platform_doc)
                movie_detail['streaming_platforms'].append(platform_doc)

        # 5. Insert all records
        db.movies.insert_one(movie)
        db.movie_details.insert_one(movie_detail)

        # 6. Prepare response
        response = {
            'movie_id': movie_id,
            'title': data['title'],
            'message': 'Movie created successfully with all details'
        }

        return jsonify(response), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movie_details.route('/movie-details', methods=['POST'])
def create_movie_detail():
    """Create a new movie detail"""
    try:
        data = request.get_json()
        if not data or not data.get('movie_id') or not data.get('title'):
            return jsonify({'error': 'Movie ID and title are required'}), 400

        movie_detail = {
            'movie_id': data['movie_id'],
            'title': data['title'],
            'year': data.get('year'),
            'ua': data.get('ua'),
            'rating': data.get('rating'),
            'is_featured': data.get('is_featured', False),
            'is_latest': data.get('is_latest', False),
            'runtime': data.get('runtime'),
            'description': data.get('description'),
            'director': data.get('director'),
            'writers': data.get('writers', []),
            'studio': data.get('studio'),
            'cast_members': data.get('cast_members', []),
            'created_at': datetime.utcnow(),
            'genres': [],
            'streaming_platforms': []
        }

        # Add genres if provided
        if data.get('genres'):
            for genre in data['genres']:
                genre_doc = {
                    'id': ObjectId(genre['id']),
                    'name': genre['name']
                }
                movie_detail['genres'].append(genre_doc)

        # Add streaming platforms if provided
        if data.get('streaming_platforms'):
            for platform in data['streaming_platforms']:
                platform_doc = {
                    'platform_id': ObjectId(platform['platform_id']),
                    'platform_name': platform['platform_name'],
                    'available_until': datetime.fromisoformat(platform['available_until'].replace('Z', '+00:00')) if platform.get('available_until') else None,
                    'added_date': datetime.utcnow()
                }
                movie_detail['streaming_platforms'].append(platform_doc)
        
        db = get_db()
        result = db.movie_details.insert_one(movie_detail)
        
        # Convert ObjectId and dates to string for response
        movie_detail['_id'] = str(result.inserted_id)
        for genre in movie_detail['genres']:
            genre['id'] = str(genre['id'])
        for platform in movie_detail['streaming_platforms']:
            platform['platform_id'] = str(platform['platform_id'])
            if platform.get('available_until'):
                platform['available_until'] = platform['available_until'].isoformat()
            platform['added_date'] = platform['added_date'].isoformat()
        
        return jsonify(movie_detail), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movie_details.route('/movie-details/<movie_id>', methods=['GET'])
def get_movie_detail(movie_id):
    """Get a specific movie detail"""
    try:
        db = get_db()
        detail = db.movie_details.find_one({'movie_id': movie_id})
        
        if not detail:
            return jsonify({'error': 'Movie detail not found'}), 404
            
        # Convert ObjectId and dates to string for JSON serialization
        detail['_id'] = str(detail['_id'])
        for genre in detail.get('genres', []):
            if genre.get('id'):
                genre['id'] = str(genre['id'])
        for platform in detail.get('streaming_platforms', []):
            if platform.get('platform_id'):
                platform['platform_id'] = str(platform['platform_id'])
            if platform.get('available_until'):
                platform['available_until'] = platform['available_until'].isoformat()
            if platform.get('added_date'):
                platform['added_date'] = platform['added_date'].isoformat()
        
        return jsonify(detail), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movie_details.route('/movie-details/<movie_id>', methods=['PUT'])
def update_movie_detail(movie_id):
    """Update a movie detail"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        db = get_db()
        update_data = {}
        
        # Update basic fields if provided
        fields = ['title', 'year', 'ua', 'rating', 'is_featured', 'is_latest', 
                 'runtime', 'description', 'director', 'writers', 'studio', 'cast_members']
        for field in fields:
            if field in data:
                update_data[field] = data[field]
            
        # Update genres if provided
        if 'genres' in data:
            genres = []
            for genre in data['genres']:
                genre_doc = {
                    'id': ObjectId(genre['id']),
                    'name': genre['name']
                }
                genres.append(genre_doc)
            update_data['genres'] = genres
            
        # Update streaming platforms if provided
        if 'streaming_platforms' in data:
            platforms = []
            for platform in data['streaming_platforms']:
                platform_doc = {
                    'platform_id': ObjectId(platform['platform_id']),
                    'platform_name': platform['platform_name'],
                    'available_until': datetime.fromisoformat(platform['available_until'].replace('Z', '+00:00')) if platform.get('available_until') else None,
                    'added_date': datetime.utcnow()
                }
                platforms.append(platform_doc)
            update_data['streaming_platforms'] = platforms
        
        result = db.movie_details.update_one(
            {'movie_id': movie_id},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Movie detail not found'}), 404
            
        return jsonify({'message': 'Movie detail updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
