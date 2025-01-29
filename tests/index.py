from flask import Flask, jsonify, render_template
import os
from supabase import create_client
from datetime import datetime
import requests
from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app with correct template path
template_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, 
            template_folder=template_dir)

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Please set SUPABASE_URL and SUPABASE_KEY environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def search_movies(query):
    """Search movies using the PCMirror API"""
    encoded_query = quote(query)
    url = f"https://pcmirror.cc/pv/search.php?s={encoded_query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"API request failed: {str(e)}", "searchResult": []}

def save_to_supabase(movie):
    """Save a single movie to Supabase"""
    try:
        movie_data = {
            'movie_id': movie['id'],
            'title': movie['t'],
            'year': movie['y'],
            'runtime': movie['r'],
            'created_at': datetime.now().isoformat()
        }
        
        supabase.table('movies').insert(movie_data).execute()
        return True
    except Exception as e:
        print(f"Error saving movie {movie['t']}: {e}")
        return False

@app.route('/')
def home():
    try:
        api_data = {
            "status": "success",
            "message": "Welcome to the Movie Collection API",
            "endpoints": {
                "GET /": "API information and available endpoints",
                "GET /search/<query>": "Search movies by query and save new ones",
                "GET /movies/data": "Get all saved movies from database"
            }
        }
        return jsonify(api_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search/<query>')
def search_and_save(query):
    """Search and save movies for a specific query"""
    try:
        # Get existing movie IDs
        response = supabase.table('movies').select('movie_id').execute()
        existing_ids = {item['movie_id'] for item in response.data}
        
        # Search for movies
        results = search_movies(query)
        
        if results.get("error"):
            return jsonify({"error": results["error"]}), 400
        
        # Save new movies
        added_count = 0
        for movie in results.get('searchResult', []):
            if movie['id'] not in existing_ids:
                if save_to_supabase(movie):
                    existing_ids.add(movie['id'])
                    added_count += 1
        
        return jsonify({
            "status": "success",
            "query": query,
            "total_results": len(results.get('searchResult', [])),
            "new_movies_added": added_count
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/movies')
def get_movies():
    """Get all saved movies"""
    try:
        response = supabase.table('movies').select('*').order('created_at.desc').execute()
        return jsonify({
            "status": "success",
            "total": len(response.data),
            "movies": response.data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/stats/data')
def get_stats():
    """Get collection statistics"""
    try:
        response = supabase.table('movies').select('*').execute()
        movies = response.data
        
        years = {}
        for movie in movies:
            year = movie.get('year', 'Unknown')
            years[year] = years.get(year, 0) + 1
        
        return jsonify({
            "status": "success",
            "total_movies": len(movies),
            "movies_by_year": years,
            "last_updated": max(movie['created_at'] for movie in movies) if movies else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
