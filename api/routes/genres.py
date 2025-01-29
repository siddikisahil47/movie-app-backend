from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from api.utils.db import get_db
from functools import wraps

genres = Blueprint('genres', __name__)

def sync_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

@genres.route('/genres/search', methods=['GET'])
def search_genres():
    """Search genres by name"""
    try:
        name = request.args.get('name', '')
        if not name:
            return jsonify({'error': 'Name parameter is required'}), 400

        db = get_db()
        collection = db['genres']
        # Using case-insensitive regex search
        genres = list(collection.find(
            {'name': {'$regex': name, '$options': 'i'}},
            {'name': 1, 'created_at': 1}
        ))

        for genre in genres:
            genre['_id'] = str(genre['_id'])
            
        return jsonify(genres), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@genres.route('/genres', methods=['POST'])
# @sync_route
def create_genre():
    """Create a new genre"""
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400

        genre = {
            'name': data['name'],
            'created_at': datetime.utcnow()
        }
        
        db = get_db()
        collection = db['genres']
        result = collection.insert_one(genre)
        
        genre['_id'] = str(result.inserted_id)
        return jsonify(genre), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@genres.route('/genres', methods=['GET'])
# @sync_route
def get_genres():
    """Get all genres"""
    try:
        db = get_db()
        # collection = db['genres']
        genres = list(db.genres.find(
            {},
            {'name': 1, 'created_at': 1}
        ))

        for genre in genres:
            genre['_id'] = str(genre['_id'])
            
        return jsonify(genres), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@genres.route('/genres/<genre_id>', methods=['GET'])
# @sync_route
def get_genre(genre_id):
    """Get a specific genre"""
    try:
        db = get_db()
        collection = db['genres']
        genre = collection.find_one({'_id': ObjectId(genre_id)})
        
        if not genre:
            return jsonify({'error': 'Genre not found'}), 404
            
        genre['_id'] = str(genre['_id'])
        
        return jsonify(genre), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@genres.route('/genres/<genre_id>', methods=['PUT'])
# @sync_route
def update_genre(genre_id):
    """Update a genre"""
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
            
        db = get_db()
        collection = db['genres']
        result = collection.update_one(
            {'_id': ObjectId(genre_id)},
            {'$set': {'name': data['name']}}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Genre not found'}), 404
            
        return jsonify({'message': 'Genre updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@genres.route('/genres/<genre_id>', methods=['DELETE'])
# @sync_route
def delete_genre(genre_id):
    """Delete a genre"""
    try:
        db = get_db()
        collection = db['genres']
        result = collection.delete_one({'_id': ObjectId(genre_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Genre not found'}), 404
            
        return jsonify({'message': 'Genre deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@genres.route('/genres/top-movies', methods=['GET'])
def get_top_movies_by_genre():
    """Get top movies for each genre with customizable limit"""
    try:
        db = get_db()
        limit = int(request.args.get('limit', 15))  # Default to 15 if not specified
        quality = request.args.get('quality', '720')  # Default image quality
        
        # Validate limit
        if limit < 1:
            return jsonify({'error': 'Limit must be greater than 0'}), 400
        
        # Get all genres first
        genres = list(db.genres.find({}, {'name': 1}))
        
        result = {}
        for genre in genres:
            # Find movies for this genre, sorted by rating
            movies = list(db.movie_details.find(
                {'genres.id': genre['_id']},
                {
                    'movie_id': 1,
                    'title': 1,
                    'year': 1,
                    'rating': 1,
                    'runtime': 1,
                    'director': 1,
                    'description': 1
                }
            ).sort('rating', -1).limit(limit))  # Use the provided limit
            
            # Convert ObjectId to string and add image URLs
            for movie in movies:
                movie['_id'] = str(movie['_id'])
                movie['image_url'] = f"https://imgcdn.media/pv/{quality}/{movie['movie_id']}.jpg"
            
            # Add to result dictionary
            result[genre['name']] = movies
        
        return jsonify(result), 200
    except ValueError:
        return jsonify({'error': 'Invalid limit parameter'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@genres.route('/genres/<genre_name>/movies', methods=['GET'])
def get_movies_by_genre_name(genre_name):
    """Get all movies for a specific genre"""
    try:
        db = get_db()
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        sort_by = request.args.get('sort_by', 'rating')  # default sort by rating
        sort_order = request.args.get('sort_order', 'desc')  # default descending
        quality = request.args.get('quality', '720')  # Default image quality
        
        # Find genre by name (case-insensitive)
        genre = db.genres.find_one({'name': {'$regex': f'^{genre_name}$', '$options': 'i'}})
        if not genre:
            return jsonify({'error': 'Genre not found'}), 404
            
        # Prepare sort parameters
        sort_direction = -1 if sort_order.lower() == 'desc' else 1
        sort_field = {
            'rating': 'rating',
            'title': 'title',
            'year': 'year',
            'runtime': 'runtime'
        }.get(sort_by, 'rating')
        
        # Calculate skip value for pagination
        skip = (page - 1) * per_page
        
        # Find movies for this genre with pagination
        movies = list(db.movie_details.find(
            {'genres.id': genre['_id']},
            {
                'movie_id': 1,
                'title': 1,
                'year': 1,
                'rating': 1,
                'runtime': 1,
                'director': 1,
                'description': 1,
                'cast_members': 1,
                'streaming_platforms': 1,
                'is_featured': 1,
                'is_latest': 1
            }
        ).sort(sort_field, sort_direction).skip(skip).limit(per_page))
        
        # Get total count for pagination
        total_movies = db.movie_details.count_documents({'genres.id': genre['_id']})
        
        # Convert ObjectId to string and add image URLs
        for movie in movies:
            movie['_id'] = str(movie['_id'])
            movie['image_url'] = f"https://imgcdn.media/pv/{quality}/{movie['movie_id']}.jpg"
            # Convert platform IDs if present
            if 'streaming_platforms' in movie:
                for platform in movie['streaming_platforms']:
                    if 'platform_id' in platform:
                        platform['platform_id'] = str(platform['platform_id'])
        
        response = {
            'genre': genre['name'],
            'total_movies': total_movies,
            'total_pages': (total_movies + per_page - 1) // per_page,
            'current_page': page,
            'per_page': per_page,
            'movies': movies
        }
        
        return jsonify(response), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid pagination parameters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@genres.route('/genres/with-movies', methods=['GET'])
def get_genres_with_movies():
    try:
        db = get_db()
        limit = min(int(request.args.get('limit', 10)), 20)  # Cap at 20 movies per genre
        page = max(int(request.args.get('page', 1)), 1)
        per_page = min(int(request.args.get('per_page', 20)), 50)  # Cap at 50 genres per page
        quality = request.args.get('quality', '720')
        
        # Get total genres count for pagination
        total_genres = db.genres.count_documents({})
        
        # Get genres with pagination, sorted by movie count
        pipeline = [
            {
                '$lookup': {
                    'from': 'movie_details',
                    'localField': '_id',
                    'foreignField': 'genres.id',
                    'as': 'movie_count'
                }
            },
            {
                '$addFields': {
                    'movieCount': { '$size': '$movie_count' }
                }
            },
            { '$sort': { 'movieCount': -1 } },
            { '$skip': (page - 1) * per_page },
            { '$limit': per_page }
        ]
        
        genres = list(db.genres.aggregate(pipeline))
        
        result = []
        for genre in genres:
            movies = list(db.movie_details.find(
                {'genres.id': genre['_id']},
                {
                    'movie_id': 1,
                    'title': 1,
                    'description': 1,
                    'rating': 1,
                    'year': 1,
                    'runtime': 1,
                    'director': 1,
                    'is_featured': 1,
                    'is_latest': 1,
                    'streaming_platforms': 1
                }
            ).sort([('rating', -1), ('year', -1)]).limit(limit))
            
            # Process movies...
            for movie in movies:
                movie['_id'] = str(movie['_id'])
                movie['image_url'] = f"https://imgcdn.media/pv/{quality}/{movie['movie_id']}.jpg"
                if 'streaming_platforms' in movie:
                    for platform in movie['streaming_platforms']:
                        if 'platform_id' in platform:
                            platform['platform_id'] = str(platform['platform_id'])
            
            result.append({
                '_id': str(genre['_id']),
                'name': genre['name'],
                'movies': movies
            })
        
        response = {
            'genres': result,
            'pagination': {
                'total_genres': total_genres,
                'total_pages': (total_genres + per_page - 1) // per_page,
                'current_page': page,
                'per_page': per_page
            }
        }
        
        return jsonify(response), 200, {
            'Cache-Control': 'public, max-age=300',
            'Vary': 'Accept-Encoding'
        }
    except ValueError:
        return jsonify({'error': 'Invalid parameters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@genres.route('/movie-details/similar', methods=['GET'])
def get_similar_movies():
    """Get similar movies based on genres, excluding the current movie"""
    try:
        db = get_db()
        genres = request.args.get('genres', '').split(',')
        exclude_id = request.args.get('exclude')
        limit = int(request.args.get('limit', 10))

        if not genres or not exclude_id:
            return jsonify({'error': 'Genres and exclude parameters are required'}), 400

        movies = list(db.movie_details.find(
            {
                '$and': [
                    {'movie_id': {'$ne': exclude_id}},
                    {'genres.name': {'$in': genres}}
                ]
            },
            {
                'movie_id': 1,
                'title': 1,
                'description': 1,
                'year': 1,
                'rating': 1,
                'runtime': 1,
                'director': 1,
                'cast_members': 1,
                'genres': 1,
                'is_featured': 1,
                'created_at': 1
            }
        ).sort('rating', -1).limit(limit))

        # Convert all ObjectId fields to strings
        for movie in movies:
            movie['_id'] = str(movie['_id'])
            # Convert genre ObjectIds
            if 'genres' in movie:
                for genre in movie['genres']:
                    if 'id' in genre:
                        genre['id'] = str(genre['id'])

        if not movies:
            return jsonify([]), 200

        return jsonify(movies), 200

    except Exception as e:
        print(f"Error in get_similar_movies: {str(e)}")
        return jsonify({'error': str(e)}), 500 