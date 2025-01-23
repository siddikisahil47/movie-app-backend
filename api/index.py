from flask import Flask, jsonify, render_template_string
import os
from supabase import create_client
from datetime import datetime
import requests
from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Please set SUPABASE_URL and SUPABASE_KEY environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie Collection</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <!-- Navigation -->
    <nav class="bg-gray-800 text-white p-4">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-xl font-bold">Movie Collection</a>
            <div class="space-x-4">
                <a href="/" class="hover:text-gray-300">Home</a>
                <a href="/movies" class="hover:text-gray-300">Movies</a>
                <a href="/stats" class="hover:text-gray-300">Stats</a>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto p-4">
        {% if request.endpoint == 'home' %}
            <div class="max-w-4xl mx-auto">
                <h1 class="text-3xl font-bold mb-8 text-center">Movie Search</h1>
                
                <!-- Search Form -->
                <div class="bg-white p-6 rounded-lg shadow-md mb-8">
                    <form id="searchForm" class="space-y-4">
                        <div>
                            <input type="text" id="searchQuery" 
                                   class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-purple-400"
                                   placeholder="Enter movie title...">
                        </div>
                        <button type="submit" 
                                class="w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white py-3 px-4 rounded-md hover:from-purple-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transform transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] shadow-md">
                            Search Movies
                        </button>
                    </form>
                </div>

                <!-- Search Results -->
                <div id="results" class="bg-white p-6 rounded-lg shadow-md hidden">
                    <h2 class="text-xl font-semibold mb-4">Search Results</h2>
                    <div id="resultsContent" class="space-y-2">
                        <!-- Results will be inserted here -->
                    </div>
                </div>
            </div>

            <script>
            document.getElementById('searchForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const query = document.getElementById('searchQuery').value.trim();
                if (!query) return;

                const resultsDiv = document.getElementById('results');
                const resultsContent = document.getElementById('resultsContent');
                resultsContent.innerHTML = '<p class="text-gray-600">Searching...</p>';
                resultsDiv.classList.remove('hidden');

                try {
                    const response = await fetch(`/search/${encodeURIComponent(query)}`);
                    const data = await response.json();

                    if (data.error) {
                        resultsContent.innerHTML = `<p class="text-red-500">Error: ${data.error}</p>`;
                    } else {
                        resultsContent.innerHTML = `
                            <div class="space-y-2">
                                <p class="text-purple-600 font-medium">Found ${data.total_results} results</p>
                                <p class="text-indigo-600 font-medium">Added ${data.new_movies_added} new movies to the collection</p>
                            </div>
                        `;
                    }
                } catch (error) {
                    resultsContent.innerHTML = `<p class="text-red-500">Error: ${error.message}</p>`;
                }
            });
            </script>
        {% endif %}

        {% if request.endpoint == 'movies_page' %}
            <div class="max-w-6xl mx-auto">
                <h1 class="text-3xl font-bold mb-8 text-center">Movie Collection</h1>
                
                <!-- Search and Filter -->
                <div class="bg-white p-4 rounded-lg shadow-md mb-6">
                    <input type="text" id="movieFilter" 
                           class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-purple-400"
                           placeholder="Filter movies...">
                </div>

                <!-- Movies Table -->
                <div class="bg-white rounded-lg shadow-md overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Year</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Runtime</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Added</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200" id="moviesList">
                                <tr>
                                    <td colspan="4" class="px-6 py-4 text-center text-gray-500">Loading movies...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <script>
            async function loadMovies() {
                try {
                    const response = await fetch('/movies/data');
                    const data = await response.json();
                    
                    if (data.error) {
                        document.getElementById('moviesList').innerHTML = `
                            <tr><td colspan="4" class="px-6 py-4 text-center text-red-500">Error: ${data.error}</td></tr>
                        `;
                        return;
                    }

                    if (!data.movies || data.movies.length === 0) {
                        document.getElementById('moviesList').innerHTML = `
                            <tr><td colspan="4" class="px-6 py-4 text-center text-gray-500">No movies found</td></tr>
                        `;
                        return;
                    }

                    renderMovies(data.movies);
                } catch (error) {
                    document.getElementById('moviesList').innerHTML = `
                        <tr><td colspan="4" class="px-6 py-4 text-center text-red-500">Error loading movies: ${error.message}</td></tr>
                    `;
                }
            }

            function renderMovies(movies) {
                const moviesList = document.getElementById('moviesList');
                moviesList.innerHTML = movies.map(movie => `
                    <tr class="hover:bg-gray-50">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="text-sm font-medium text-gray-900">${movie.title}</div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="text-sm text-gray-500">${movie.year || 'N/A'}</div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="text-sm text-gray-500">${movie.runtime || 'N/A'}</div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="text-sm text-gray-500">${new Date(movie.created_at).toLocaleDateString()}</div>
                        </td>
                    </tr>
                `).join('');
            }

            document.getElementById('movieFilter').addEventListener('input', function(e) {
                const filter = e.target.value.toLowerCase();
                const rows = document.querySelectorAll('#moviesList tr');
                
                rows.forEach(row => {
                    const title = row.querySelector('td:first-child')?.textContent.toLowerCase();
                    if (title) {
                        row.style.display = title.includes(filter) ? '' : 'none';
                    }
                });
            });

            loadMovies();
            </script>
        {% endif %}

        {% if request.endpoint == 'stats_page' %}
            <div class="max-w-6xl mx-auto">
                <h1 class="text-3xl font-bold mb-8 text-center">Collection Statistics</h1>
                
                <!-- Stats Cards -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-lg font-semibold text-gray-700 mb-2">Total Movies</h3>
                        <p class="text-3xl font-bold text-purple-600" id="totalMovies">-</p>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-lg font-semibold text-gray-700 mb-2">Latest Update</h3>
                        <p class="text-xl text-gray-600" id="lastUpdated">-</p>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-lg font-semibold text-gray-700 mb-2">Unique Years</h3>
                        <p class="text-3xl font-bold text-indigo-600" id="uniqueYears">-</p>
                    </div>
                </div>

                <!-- Charts -->
                <div class="grid grid-cols-1 gap-6">
                    <!-- Movies by Year Chart -->
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-lg font-semibold text-gray-700 mb-4">Movies by Year</h3>
                        <div class="h-96">
                            <canvas id="yearChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>

            <script>
            let yearChart;

            async function loadStats() {
                try {
                    const response = await fetch('/stats/data');
                    const data = await response.json();
                    
                    if (data.error) {
                        console.error('Error:', data.error);
                        return;
                    }

                    updateStats(data);
                    createYearChart(data.movies_by_year);
                } catch (error) {
                    console.error('Error loading stats:', error);
                }
            }

            function updateStats(data) {
                document.getElementById('totalMovies').textContent = data.total_movies;
                document.getElementById('uniqueYears').textContent = Object.keys(data.movies_by_year).length;
                
                const lastUpdated = data.last_updated ? 
                    new Date(data.last_updated).toLocaleString() : 
                    'Never';
                document.getElementById('lastUpdated').textContent = lastUpdated;
            }

            function createYearChart(moviesByYear) {
                const ctx = document.getElementById('yearChart').getContext('2d');
                
                // Sort years
                const years = Object.keys(moviesByYear).sort();
                const counts = years.map(year => moviesByYear[year]);

                // Destroy existing chart if it exists
                if (yearChart) {
                    yearChart.destroy();
                }

                yearChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: years,
                        datasets: [{
                            label: 'Number of Movies',
                            data: counts,
                            backgroundColor: 'rgba(124, 58, 237, 0.5)',
                            borderColor: 'rgb(124, 58, 237)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    stepSize: 1
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                });
            }

            loadStats();
            </script>
        {% endif %}
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white p-4 mt-8">
        <div class="container mx-auto text-center">
            <p>&copy; 2024 Movie Collection. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

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
    return render_template_string(HTML_TEMPLATE)

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
def movies_page():
    return render_template_string(HTML_TEMPLATE)

@app.route('/movies/data')
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

@app.route('/stats')
def stats_page():
    return render_template_string(HTML_TEMPLATE)

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
