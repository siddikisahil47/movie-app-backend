import pytest
from api.models.movie import Movie, MovieDetail
from datetime import datetime

@pytest.mark.asyncio
async def test_movie_operations():
    """Test movie creation and retrieval operations."""
    # Generate unique movie_id using timestamp
    unique_id = f"test_{int(datetime.now().timestamp())}"
    
    # Test data
    movie_data = {
        "movie_id": unique_id,
        "title": "Test Movie",
        "year": "2024",
        "runtime": "120 min",
        "image_url": "http://example.com/image.jpg",
        "poster_url": "http://example.com/poster.jpg"
    }
    
    movie_details = {
        "title": "Test Movie",
        "year": "2024",
        "ua": "PG-13",
        "match": "95%",
        "runtime": "120 min",
        "hdsd": "HD",
        "type": "Movie",
        "director": "Test Director",
        "writer": "Test Writer",
        "producers": "Test Producer",
        "studio": "Test Studio",
        "cast_members": "Actor 1, Actor 2",
        "genre": "Action",
        "description": "Test description",
        "languages": ["English", "Spanish"],
        "image_url": "http://example.com/image.jpg",
        "poster_url": "http://example.com/poster.jpg"
    }
    
    try:
        # Test 1: Create movie with details
        result = await MovieDetail.create_with_movie(movie_data, movie_details)
        assert result is not None
        assert result['movie_id'] == movie_data['movie_id']
        assert result['title'] == movie_data['title']
        assert result['details'] is not None
        print("✅ Movie creation successful")
        
        # Test 2: Fetch movie by movie_id
        movie = await Movie.find_by_movie_id(movie_data['movie_id'])
        assert movie is not None
        assert movie['title'] == movie_data['title']
        print("✅ Movie retrieval successful")
        
        # Test 3: Fetch movie details
        details = await MovieDetail.find_by_movie_id(movie_data['movie_id'])
        assert details is not None
        assert details['director'] == movie_details['director']
        print("✅ Movie details retrieval successful")
        
        # Test 4: Get full movie
        full_movie = await MovieDetail.get_full_movie(movie_data['movie_id'])
        assert full_movie is not None
        assert full_movie['details'] is not None
        assert full_movie['details']['director'] == movie_details['director']
        print("✅ Full movie retrieval successful")
        
        # Test 5: Search by title
        search_results = await Movie.search_by_title("Test")
        assert len(search_results) > 0
        assert any(m['movie_id'] == movie_data['movie_id'] for m in search_results)
        print("✅ Movie search successful")
        
        print("\n✅ All tests passed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise 