from typing import Dict, Optional, List
from . import BaseModel

class Movie(BaseModel):
    """Movie model for database operations."""
    table_name = "movies"
    
    @classmethod
    async def find_by_movie_id(cls, movie_id: str) -> Optional[Dict]:
        """Find a movie by movie_id."""
        try:
            response = cls.get_db().table(cls.table_name)\
                .select("*")\
                .eq("movie_id", movie_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error finding movie by movie_id: {str(e)}")
    
    @classmethod
    async def search_by_title(cls, title: str) -> List[Dict]:
        """Search movies by title."""
        try:
            response = cls.get_db().table(cls.table_name)\
                .select("*")\
                .ilike("title", f"%{title}%")\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error searching movies: {str(e)}")
    
    @classmethod
    def validate_movie_data(cls, data: Dict) -> Dict:
        """Validate movie data before creation/update."""
        required_fields = ['movie_id', 'title']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        return data

class MovieDetail(BaseModel):
    """MovieDetail model for database operations."""
    table_name = "movie_details"
    
    @classmethod
    async def find_by_movie_id(cls, movie_id: str) -> Optional[Dict]:
        """Find movie details by movie_id."""
        try:
            response = cls.get_db().table(cls.table_name)\
                .select("*")\
                .eq("movie_id", movie_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error finding movie details by movie_id: {str(e)}")
    
    @classmethod
    async def create_with_movie(cls, movie_data: Dict, detail_data: Dict) -> Dict:
        """Create both movie and its details."""
        try:
            # First create the movie
            movie = await Movie.create(Movie.validate_movie_data(movie_data))
            
            # Then create the movie details
            detail_data['movie_id'] = movie['movie_id']
            detail = await cls.create(detail_data)
            
            return {**movie, 'details': detail}
        except Exception as e:
            raise Exception(f"Error creating movie with details: {str(e)}")
    
    @classmethod
    async def get_full_movie(cls, movie_id: str) -> Optional[Dict]:
        """Get movie with its details."""
        try:
            movie = await Movie.find_by_movie_id(movie_id)
            if not movie:
                return None
                
            details = await cls.find_by_movie_id(movie_id)
            return {**movie, 'details': details} if details else movie
        except Exception as e:
            raise Exception(f"Error getting full movie: {str(e)}")
            
    @classmethod
    async def get_all_genres(cls) -> List[str]:
        """Get all unique genres from the database."""
        try:
            # Get all non-null genres
            response = cls.get_db().table(cls.table_name)\
                .select('genre')\
                .neq('genre', None)\
                .execute()
            
            # Process genres to get unique values
            all_genres = set()
            for item in response.data:
                genre = item.get('genre')
                if genre:
                    # Handle both comma and pipe separated genres
                    genres = [g.strip() for g in genre.replace('|', ',').split(',')]
                    # Filter out empty strings
                    genres = [g for g in genres if g]
                    all_genres.update(genres)
            
            # Return sorted list of genres
            return sorted(list(filter(None, all_genres)))
        except Exception as e:
            raise Exception(f"Error getting genres: {str(e)}")
            
    @classmethod
    async def get_featured_movies(cls, limit: int = 10) -> List[Dict]:
        """Get featured movies with high match scores and recent releases."""
        try:
            # Get movies with high match scores and recent releases
            response = cls.get_db().table(cls.table_name)\
                .select('*, movies!inner(*)')\
                .order('match', desc=True)\
                .limit(limit)\
                .execute()
            
            # Process and format the response
            featured_movies = []
            for item in response.data:
                if 'movies' in item:
                    movie_data = item.pop('movies')
                    featured_movies.append({**movie_data, 'details': item})
            
            return featured_movies
        except Exception as e:
            raise Exception(f"Error getting featured movies: {str(e)}")