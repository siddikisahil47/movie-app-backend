[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fpython%2Fflask3&demo-title=Flask%203%20%2B%20Vercel&demo-description=Use%20Flask%203%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fflask3-python-template.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994156/random/flask.png)

# Movie App Backend

A Flask-based RESTful API for managing movies with Supabase integration.

## Features

- RESTful API endpoints for movies
- User authentication and authorization
- Supabase integration for data storage
- Rate limiting
- API documentation

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/movie-app-backend.git
cd movie-app-backend
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

## Development

Run the development server:
```bash
flask run --debug
```

## Testing

Run tests:
```bash
pytest
```

## API Documentation

### Endpoints

- `GET /api/v1/movies`: List all movies
- `GET /api/v1/movies/<id>`: Get movie details
- `POST /api/v1/movies`: Create a new movie
- `PUT /api/v1/movies/<id>`: Update a movie
- `DELETE /api/v1/movies/<id>`: Delete a movie

### Authentication

- `POST /api/v1/auth/register`: Register new user
- `POST /api/v1/auth/login`: Login user

## Deployment

The application is configured for deployment on platforms like Heroku using Gunicorn.

## License

MIT

## Demo

https://flask-python-template.vercel.app/

## How it Works

This example uses the Web Server Gateway Interface (WSGI) with Flask to enable handling requests on Vercel with Serverless Functions.

## Running Locally

```bash
npm i -g vercel
vercel dev
```

Your Flask application is now available at `http://localhost:3000`.

## One-Click Deploy

Deploy the example using [Vercel](https://vercel.com?utm_source=github&utm_medium=readme&utm_campaign=vercel-examples):

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fpython%2Fflask3&demo-title=Flask%203%20%2B%20Vercel&demo-description=Use%20Flask%203%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fflask3-python-template.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994156/random/flask.png)
