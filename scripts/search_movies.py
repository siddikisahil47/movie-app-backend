import requests
import json
import os
import time
from datetime import datetime
from urllib.parse import quote
from itertools import product
import string
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Please set SUPABASE_URL and SUPABASE_KEY in .env file")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def search_movies(query):
    """
    Search movies using the PCMirror API
    """
    # URL encode the query
    encoded_query = quote(query)
    url = f"https://pcmirror.cc/pv/search.php?s={encoded_query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"API request failed: {str(e)}", "searchResult": []}

def load_existing_movies():
    """
    Load existing movies from Supabase to prevent duplicates
    """
    try:
        response = supabase.table('movies').select('movie_id').execute()
        existing_ids = {item['movie_id'] for item in response.data}
        return existing_ids
    except Exception as e:
        print(f"Error loading existing movies: {e}")
        return set()

def save_to_supabase(movie):
    """
    Save a single movie to Supabase
    """
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

def save_results(new_results, existing_movie_ids):
    """
    Save unique search results to Supabase
    """
    added_count = 0
    
    for movie in new_results.get('searchResult', []):
        if movie['id'] not in existing_movie_ids:
            if save_to_supabase(movie):
                existing_movie_ids.add(movie['id'])
                added_count += 1
    
    if added_count > 0:
        print(f"Added {added_count} new unique movies to Supabase")
    
    return added_count

def generate_search_queries(min_length=1, max_length=3):
    """
    Generate combinations of letters and numbers for searching
    """
    # Create character set (a-z, 0-9)
    chars = string.ascii_lowercase + string.digits
    
    for length in range(min_length, max_length + 1):
        for combo in product(chars, repeat=length):
            yield ''.join(combo)

def main():
    print("Starting automatic movie search...")
    existing_movie_ids = load_existing_movies()
    print(f"Loaded {len(existing_movie_ids)} existing movies from Supabase")
    
    total_searches = 0
    total_new_movies = 0
    
    try:
        for query in generate_search_queries(min_length=1, max_length=2):
            print(f"\nSearching for: {query}")
            results = search_movies(query)
            
            if results.get("error"):
                print(f"Error: {results['error']}")
                continue
            
            new_movies = save_results(results, existing_movie_ids)
            total_new_movies += new_movies
            total_searches += 1
            
            # Add a small delay to avoid overwhelming the API
            time.sleep(1)
            
            print(f"Progress: Completed {total_searches} searches, Found {total_new_movies} new movies")
            
    except KeyboardInterrupt:
        print("\nSearch interrupted by user")
    finally:
        print(f"\nSearch completed:")
        print(f"Total searches performed: {total_searches}")
        print(f"Total unique movies found: {total_new_movies}")

if __name__ == "__main__":
    main() 