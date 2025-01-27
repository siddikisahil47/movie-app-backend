# Movie Backend API Documentation

## Genres API

### 1. Search Genres

```http
GET /genres/search?name={name}
```

Search for genres by name.

**Query Parameters:**

- `name` (required): Genre name to search for

**Response:** 200 OK

```json
[
  {
    "_id": "string",
    "name": "string",
    "created_at": "timestamp"
  }
]
```

### 2. Create Genre

```http
POST /genres
```

Create a new genre.

**Request Body:**

```json
{
  "name": "string"
}
```

**Response:** 201 Created

```json
{
  "_id": "string",
  "name": "string",
  "created_at": "timestamp"
}
```

### 3. Get All Genres

```http
GET /genres
```

Get a list of all genres.

**Response:** 200 OK

```json
[
  {
    "_id": "string",
    "name": "string",
    "created_at": "timestamp"
  }
]
```

### 4. Get Genre by ID

```http
GET /genres/{genre_id}
```

Get details of a specific genre.

**Response:** 200 OK

```json
{
  "_id": "string",
  "name": "string",
  "created_at": "timestamp"
}
```

### 5. Update Genre

```http
PUT /genres/{genre_id}
```

Update a genre's name.

**Request Body:**

```json
{
  "name": "string"
}
```

**Response:** 200 OK

```json
{
  "message": "Genre updated successfully"
}
```

### 6. Delete Genre

```http
DELETE /genres/{genre_id}
```

Delete a genre.

**Response:** 200 OK

```json
{
  "message": "Genre deleted successfully"
}
```

### 7. Get Top Movies by Genre

```http
GET /genres/top-movies
```

**Query Parameters:**

- `limit` (optional): Number of movies per genre (default: 15)
- `quality` (optional): Image quality (default: 720)

**Response:** 200 OK

```json
{
  "Action": [
    {
      "movie_id": "string",
      "title": "string",
      "year": "number",
      "rating": "number",
      "runtime": "string",
      "director": "string",
      "description": "string",
      "image_url": "string"
    }
  ]
}
```

### 8. Get Movies by Genre Name

```http
GET /genres/{genre_name}/movies
```

**Query Parameters:**

- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20)
- `sort_by` (optional): Field to sort by (options: rating, title, year, runtime) (default: rating)
- `sort_order` (optional): Sort direction (asc/desc) (default: desc)
- `quality` (optional): Image quality (default: 720)

**Response:** 200 OK

```json
{
  "genre": "string",
  "total_movies": "number",
  "total_pages": "number",
  "current_page": "number",
  "per_page": "number",
  "movies": [
    {
      "movie_id": "string",
      "title": "string",
      "year": "number",
      "rating": "number",
      "runtime": "string",
      "director": "string",
      "description": "string",
      "cast_members": ["string"],
      "streaming_platforms": [
        {
          "platform_id": "string",
          "platform_name": "string",
          "available_until": "timestamp"
        }
      ],
      "is_featured": "boolean",
      "is_latest": "boolean",
      "image_url": "string"
    }
  ]
}
```

### 9. Get Genres with Movies

```http
GET /genres/with-movies
```

**Query Parameters:**

- `limit` (optional): Number of movies per genre (default: 10)
- `page` (optional): Page number for genres pagination (default: 1)
- `per_page` (optional): Number of genres per page (default: 20)
- `quality` (optional): Image quality (default: 720)

**Response:** 200 OK

```json
{
  "genres": [
    {
      "_id": "string",
      "name": "string",
      "movies": [
        {
          "_id": "string",
          "movie_id": "string",
          "title": "string",
          "description": "string",
          "poster_url": "string",
          "rating": "number",
          "year": "number",
          "runtime": "string",
          "director": "string",
          "is_featured": "boolean",
          "is_latest": "boolean",
          "streaming_platforms": [
            {
              "platform_id": "string",
              "platform_name": "string",
              "available_until": "timestamp"
            }
          ],
          "image_url": "string"
        }
      ]
    }
  ],
  "pagination": {
    "total_genres": "number",
    "total_pages": "number",
    "current_page": "number",
    "per_page": "number"
  }
}
```

**Headers:**

- `Cache-Control: public, max-age=300` (5 minutes cache)
- `Vary: Accept-Encoding`

**Notes:**

1. Movies are sorted by rating in descending order
2. Response is cached for 5 minutes
3. Pagination is applied to genres, not movies
4. Each genre includes its top N rated movies

## Movies API

### 1. Create Complete Movie

```http
POST /movies/complete
```

Create a new movie with all details, genres, and streaming platforms.

**Request Body:**

```json
{
  "title": "string",
  "year": "number",
  "runtime": "string",
  "ua": "string",
  "rating": "number",
  "is_featured": "boolean",
  "is_latest": "boolean",
  "description": "string",
  "director": "string",
  "writers": ["string"],
  "studio": "string",
  "cast_members": ["string"],
  "genres": [
    {
      "name": "string"
    }
  ],
  "streaming_platforms": [
    {
      "platform_name": "string",
      "available_until": "timestamp"
    }
  ]
}
```

**Response:** 201 Created

```json
{
  "movie_id": "string",
  "title": "string",
  "message": "Movie created successfully with all details"
}
```

### 2. Create Movie Detail

```http
POST /movie-details
```

Create movie details for an existing movie.

**Request Body:**

```json
{
  "movie_id": "string",
  "title": "string",
  "year": "number",
  "ua": "string",
  "rating": "number",
  "is_featured": "boolean",
  "is_latest": "boolean",
  "runtime": "string",
  "description": "string",
  "director": "string",
  "writers": ["string"],
  "studio": "string",
  "cast_members": ["string"],
  "genres": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp"
    }
  ]
}
```

**Response:** 201 Created

```json
{
  "_id": "string",
  "movie_id": "string",
  "title": "string",
  "year": "number",
  "ua": "string",
  "rating": "number",
  "is_featured": "boolean",
  "is_latest": "boolean",
  "runtime": "string",
  "description": "string",
  "director": "string",
  "writers": ["string"],
  "studio": "string",
  "cast_members": ["string"],
  "genres": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp",
      "added_date": "timestamp"
    }
  ],
  "created_at": "timestamp"
}
```

### 3. Get Movie Detail

```http
GET /movie-details/{movie_id}
```

Get details of a specific movie.

**Response:** 200 OK

```json
{
  "_id": "string",
  "movie_id": "string",
  "title": "string",
  "year": "number",
  "ua": "string",
  "rating": "number",
  "is_featured": "boolean",
  "is_latest": "boolean",
  "runtime": "string",
  "description": "string",
  "director": "string",
  "writers": ["string"],
  "studio": "string",
  "cast_members": ["string"],
  "genres": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp",
      "added_date": "timestamp"
    }
  ],
  "created_at": "timestamp"
}
```

### 4. Update Movie Detail

```http
PUT /movie-details/{movie_id}
```

Update details of a specific movie.

**Request Body:**

```json
{
  "title": "string",
  "year": "number",
  "ua": "string",
  "rating": "number",
  "is_featured": "boolean",
  "is_latest": "boolean",
  "runtime": "string",
  "description": "string",
  "director": "string",
  "writers": ["string"],
  "studio": "string",
  "cast_members": ["string"],
  "genres": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp"
    }
  ]
}
```

**Response:** 200 OK

```json
{
  "message": "Movie detail updated successfully"
}
```

### 5. Search Movies

```http
GET /movies/search?title={title}
```

Search movies by title.

**Query Parameters:**

- `title` (required): Movie title to search for

**Response:** 200 OK

```json
[
  {
    "movie_id": "string",
    "title": "string",
    "year": "number",
    "runtime": "string",
    "streaming_platforms": [
      {
        "platform_id": "string",
        "platform_name": "string",
        "available_until": "timestamp",
        "added_date": "timestamp"
      }
    ]
  }
]
```

## Streaming Platforms API

### 1. Create Platform

```http
POST /platforms
```

Create a new streaming platform.

**Request Body:**

```json
{
  "name": "string",
  "active": "boolean"
}
```

**Response:** 201 Created

```json
{
  "_id": "string",
  "name": "string",
  "active": "boolean",
  "created_at": "timestamp"
}
```

### 2. Get All Platforms

```http
GET /platforms
```

Get a list of all streaming platforms.

**Response:** 200 OK

```json
[
  {
    "_id": "string",
    "name": "string",
    "active": "boolean"
  }
]
```

### 3. Get Platform

```http
GET /platforms/{platform_id}
```

Get details of a specific streaming platform.

**Response:** 200 OK

```json
{
  "_id": "string",
  "name": "string",
  "active": "boolean"
}
```

### 4. Update Platform

```http
PUT /platforms/{platform_id}
```

Update a streaming platform.

**Request Body:**

```json
{
  "name": "string",
  "active": "boolean"
}
```

**Response:** 200 OK

```json
{
  "message": "Platform updated successfully"
}
```

### 5. Delete Platform

```http
DELETE /platforms/{platform_id}
```

Delete a streaming platform.

**Response:** 200 OK

```json
{
  "message": "Platform deleted successfully"
}
```

### 6. Search Platforms

```http
GET /platforms/search?name={name}
```

Search streaming platforms by name.

**Query Parameters:**

- `name` (required): Platform name to search for

**Response:** 200 OK

```json
[
  {
    "_id": "string",
    "name": "string",
    "active": "boolean",
    "created_at": "timestamp"
  }
]
```

## Error Responses

All endpoints can return the following error responses:

### 400 Bad Request

```json
{
  "error": "Error message describing the issue"
}
```

### 404 Not Found

```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal server error message"
}
```

## Rate Limiting

- Default rate limit: 100 requests per minute per IP
- Rate limit headers are included in responses:
  - `X-RateLimit-Limit`: Total requests allowed per window
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Time when the rate limit resets

## Authentication

Currently, these endpoints don't require authentication. Future versions may implement authentication requirements.

## Notes

1. All timestamps are in ISO 8601 format
2. All IDs are returned as strings
3. Pagination is zero-based
4. Sort orders are case-insensitive
5. Genre names in URLs are case-insensitive

## Basic Movies API

### 1. Create Movie

```http
POST /movies
```

Create a new basic movie.

**Request Body:**

```json
{
  "title": "string",
  "year": "number",
  "runtime": "string",
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp",
      "added_date": "timestamp"
    }
  ]
}
```

**Response:** 201 Created

```json
{
  "_id": "string",
  "movie_id": "string",
  "title": "string",
  "year": "number",
  "runtime": "string",
  "created_at": "timestamp",
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp",
      "added_date": "timestamp"
    }
  ]
}
```

### 2. Get All Movies

```http
GET /movies
```

Get a list of all movies.

**Response:** 200 OK

```json
[
  {
    "_id": "string",
    "movie_id": "string",
    "title": "string",
    "year": "number",
    "runtime": "string",
    "created_at": "timestamp",
    "streaming_platforms": [
      {
        "platform_id": "string",
        "platform_name": "string",
        "available_until": "timestamp",
        "added_date": "timestamp"
      }
    ]
  }
]
```

### 3. Get Movie by ID

```http
GET /movies/{movie_id}
```

Get details of a specific movie.

**Response:** 200 OK

```json
{
  "_id": "string",
  "movie_id": "string",
  "title": "string",
  "year": "number",
  "runtime": "string",
  "created_at": "timestamp",
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp",
      "added_date": "timestamp"
    }
  ]
}
```

### 4. Update Movie

```http
PUT /movies/{movie_id}
```

Update a movie's basic information.

**Request Body:**

```json
{
  "title": "string",
  "year": "number",
  "runtime": "string",
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp",
      "added_date": "timestamp"
    }
  ]
}
```

**Response:** 200 OK

```json
{
  "message": "Movie updated successfully"
}
```

### 5. Delete Movie

```http
DELETE /movies/{movie_id}
```

Delete a movie.

**Response:** 200 OK

```json
{
  "message": "Movie deleted successfully"
}
```

### 6. Search Movies

```http
GET /movies/search?title={title}
```

Search movies by title.

**Query Parameters:**

- `title` (required): Movie title to search for (case-insensitive)

**Response:** 200 OK

```json
[
  {
    "_id": "string",
    "movie_id": "string",
    "title": "string",
    "year": "number",
    "runtime": "string",
    "created_at": "timestamp",
    "streaming_platforms": [
      {
        "platform_id": "string",
        "platform_name": "string",
        "available_until": "timestamp",
        "added_date": "timestamp"
      }
    ]
  }
]
```

## Movie Details API

### 1. Create Movie Detail

```http
POST /movie-details
```

Create detailed information for a movie.

**Request Body:**

```json
{
  "movie_id": "string",
  "title": "string",
  "year": "number",
  "ua": "string",
  "rating": "number",
  "is_featured": "boolean",
  "is_latest": "boolean",
  "runtime": "string",
  "description": "string",
  "director": "string",
  "writers": ["string"],
  "studio": "string",
  "cast_members": ["string"],
  "genres": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp"
    }
  ]
}
```

**Response:** 201 Created

```json
{
  "_id": "string",
  "movie_id": "string",
  "title": "string",
  "year": "number",
  "ua": "string",
  "rating": "number",
  "is_featured": "boolean",
  "is_latest": "boolean",
  "runtime": "string",
  "description": "string",
  "director": "string",
  "writers": ["string"],
  "studio": "string",
  "cast_members": ["string"],
  "genres": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp",
      "added_date": "timestamp"
    }
  ],
  "created_at": "timestamp"
}
```

### 2. Get Movie Detail

```http
GET /movie-details/{movie_id}
```

Get detailed information for a specific movie.

**Response:** 200 OK

```json
{
  "_id": "string",
  "movie_id": "string",
  "title": "string",
  "year": "number",
  "ua": "string",
  "rating": "number",
  "is_featured": "boolean",
  "is_latest": "boolean",
  "runtime": "string",
  "description": "string",
  "director": "string",
  "writers": ["string"],
  "studio": "string",
  "cast_members": ["string"],
  "genres": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp",
      "added_date": "timestamp"
    }
  ],
  "created_at": "timestamp"
}
```

### 3. Update Movie Detail

```http
PUT /movie-details/{movie_id}
```

Update detailed information for a movie.

**Request Body:**

```json
{
  "title": "string",
  "year": "number",
  "ua": "string",
  "rating": "number",
  "is_featured": "boolean",
  "is_latest": "boolean",
  "runtime": "string",
  "description": "string",
  "director": "string",
  "writers": ["string"],
  "studio": "string",
  "cast_members": ["string"],
  "genres": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "streaming_platforms": [
    {
      "platform_id": "string",
      "platform_name": "string",
      "available_until": "timestamp"
    }
  ]
}
```

**Response:** 200 OK

```json
{
  "message": "Movie detail updated successfully"
}
```

### 4. Create Complete Movie

```http
POST /movies/complete
```

Create a movie with all its details, genres, and streaming platforms in one request.

**Request Body:**

```json
{
  "title": "string",
  "year": "number",
  "runtime": "string",
  "ua": "string",
  "rating": "number",
  "is_featured": "boolean",
  "is_latest": "boolean",
  "description": "string",
  "director": "string",
  "writers": ["string"],
  "studio": "string",
  "cast_members": ["string"],
  "genres": [
    {
      "name": "string"
    }
  ],
  "streaming_platforms": [
    {
      "platform_name": "string",
      "available_until": "timestamp"
    }
  ]
}
```

**Response:** 201 Created

```json
{
  "movie_id": "string",
  "title": "string",
  "message": "Movie created successfully with all details"
}
```

## Image URLs

All movie responses include an `image_url` field that follows this format:

```
https://imgcdn.media/pv/{quality}/{movie_id}.jpg
```

**Quality Options:**

- Can be specified via the `quality` query parameter
- Default: 720
- Common values: 361, 720, 1080
- Supports both horizontal (h) and vertical (v) variants
