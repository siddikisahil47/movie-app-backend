from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from api.utils.db import get_db

streaming = Blueprint('streaming', __name__)

@streaming.route('/platforms', methods=['POST'])
def create_platform():
    """Create a new streaming platform"""
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400

        platform = {
            'name': data['name'],
            'active': data.get('active', True),
            'created_at': datetime.utcnow()
        }
        
        db = get_db()
        result = db.streaming_platforms_list.insert_one(platform)
        
        platform['_id'] = str(result.inserted_id)
        return jsonify(platform), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@streaming.route('/platforms', methods=['GET'])
def get_platforms():
    """Get all streaming platforms"""
    try:
        db = get_db()
        platforms = list(db.streaming_platforms_list.find({}, {'name': 1, 'active': 1}))
        
        # Convert ObjectId to string for JSON serialization
        for platform in platforms:
            platform['_id'] = str(platform['_id'])
            
        return jsonify(platforms), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@streaming.route('/platforms/<platform_id>', methods=['GET'])
def get_platform(platform_id):
    """Get a specific streaming platform"""
    try:
        db = get_db()
        platform = db.streaming_platforms_list.find_one(
            {'_id': ObjectId(platform_id)},
            {'name': 1, 'active': 1}
        )
        
        if not platform:
            return jsonify({'error': 'Platform not found'}), 404
            
        platform['_id'] = str(platform['_id'])
        
        return jsonify(platform), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@streaming.route('/platforms/<platform_id>', methods=['PUT'])
def update_platform(platform_id):
    """Update a streaming platform"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        db = get_db()
        update_data = {
            'name': data.get('name'),
            'active': data.get('active')
        }
        
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        result = db.streaming_platforms_list.update_one(
            {'_id': ObjectId(platform_id)},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Platform not found'}), 404
            
        return jsonify({'message': 'Platform updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@streaming.route('/platforms/<platform_id>', methods=['DELETE'])
def delete_platform(platform_id):
    """Delete a streaming platform"""
    try:
        db = get_db()
        result = db.streaming_platforms_list.delete_one({'_id': ObjectId(platform_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Platform not found'}), 404
            
        return jsonify({'message': 'Platform deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@streaming.route('/platforms/search', methods=['GET'])
def search_platforms():
    """Search streaming platforms by name"""
    try:
        name = request.args.get('name', '')
        if not name:
            return jsonify({'error': 'Name parameter is required'}), 400

        db = get_db()
        # Using case-insensitive regex search
        platforms = list(db.streaming_platforms_list.find(
            {'name': {'$regex': name, '$options': 'i'}},
            {'name': 1, 'active': 1, 'created_at': 1}
        ))

        for platform in platforms:
            platform['_id'] = str(platform['_id'])
            
        return jsonify(platforms), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 