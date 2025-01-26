import pytest
from api import create_app
from datetime import datetime
import json

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def sample_movie_data():
    """Create sample movie data for testing."""
    unique_id = f"test_{int(datetime.now().timestamp())}"
    return {
        "movie_id": unique_id,
        "title": "Test Movie",
        "year": "2024",
        "runtime": "120 min",
        "ua": "PG-13",
        "match": "95%",
        "hdsd": "HD",
        "type": "Movie",
        "director": "Test Director",
        "writer": "Test Writer",
        "producers": "Test Producer",
        "studio": "Test Studio",
        "cast_members": "Actor 1, Actor 2",
        "genre": "Action, Adventure, Sci-Fi",
        "description": "Test description",
        "languages": ["English", "Spanish"],
        "image_url": "http://example.com/image.jpg",
        "poster_url": "http://example.com/poster.jpg"
    }

@pytest.mark.asyncio
async def test_create_movie(client, sample_movie_data):
    """Test creating a new movie."""
    response = await client.post(
        '/api/v1/movies',
        json=sample_movie_data
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['movie_id'] == sample_movie_data['movie_id']
    assert data['title'] == sample_movie_data['title']
    assert 'details' in data
    return data  # Return for use in other tests

@pytest.mark.asyncio
async def test_get_movie(client, sample_movie_data):
    """Test getting a movie by ID."""
    # First create a movie
    created_movie = await test_create_movie(client, sample_movie_data)
    
    # Then try to get it
    response = await client.get(f"/api/v1/movies/{created_movie['movie_id']}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['movie_id'] == created_movie['movie_id']
    assert data['details'] is not None

@pytest.mark.asyncio
async def test_search_movies(client, sample_movie_data):
    """Test searching movies by title."""
    # First create a movie
    await test_create_movie(client, sample_movie_data)
    
    # Then search for it
    response = await client.get("/api/v1/movies?title=Test")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0
    assert any(m['title'] == sample_movie_data['title'] for m in data)

@pytest.mark.asyncio
async def test_get_latest_movies(client, sample_movie_data):
    """Test getting latest movies."""
    # First create a movie
    await test_create_movie(client, sample_movie_data)
    
    # Then get latest movies
    response = await client.get("/api/v1/movies/latest")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0
    # The created movie should be in the results since it's the latest
    assert any(m['movie_id'] == sample_movie_data['movie_id'] for m in data)

@pytest.mark.asyncio
async def test_get_genres(client, sample_movie_data):
    """Test getting all unique genres."""
    # First create a movie with multiple genres
    await test_create_movie(client, sample_movie_data)
    
    # Then get all genres
    response = await client.get("/api/v1/genres")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    # Check if all genres from our test movie are in the results
    test_genres = [g.strip() for g in sample_movie_data['genre'].split(',')]
    for genre in test_genres:
        assert genre in data

@pytest.mark.asyncio
async def test_get_movies_by_genre(client, sample_movie_data):
    """Test getting movies by genre."""
    # First create a movie
    await test_create_movie(client, sample_movie_data)
    
    # Then get movies by genre
    response = await client.get("/api/v1/movies/genre/Action")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0
    # Verify the movie is in the results since it's an Action movie
    assert any(m['movie_id'] == sample_movie_data['movie_id'] for m in data)

@pytest.mark.asyncio
async def test_get_random_movies(client):
    """Test getting random movies."""
    response = await client.get("/api/v1/movies/random")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_health_check(client):
    """Test the health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

@pytest.mark.asyncio
async def test_invalid_movie_id(client):
    """Test getting a movie with invalid ID."""
    response = await client.get("/api/v1/movies/nonexistent_id")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

@pytest.mark.asyncio
async def test_search_without_title(client):
    """Test searching movies without providing a title."""
    response = await client.get("/api/v1/movies")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

@pytest.mark.asyncio
async def test_get_featured_movies(client, sample_movie_data):
    """Test getting featured movies."""
    # First create a movie that should be featured
    await test_create_movie(client, sample_movie_data)
    
    # Test with default limit
    response = await client.get("/api/v1/movies/featured")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Test with custom limit
    response = await client.get("/api/v1/movies/featured?limit=5")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) <= 5  # Should not exceed the requested limit
    
    # Test with invalid limit (should be capped at 20)
    response = await client.get("/api/v1/movies/featured?limit=100")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) <= 20  # Should be capped at 20 