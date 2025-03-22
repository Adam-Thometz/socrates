# Socrates App Backend

FastAPI backend for the Socrates philosophy debate application.

## Setup

1. Make sure you have Python 3.8+ installed
2. Install dependencies:
   ```
   pipenv install
   ```
3. Create a `.env` file with the following variables:
   ```
   DATABASE_URL=sqlite:///./socrates.db
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```
   
   Replace `your_anthropic_api_key_here` with your actual Anthropic API key.

## Running the Backend

1. Activate the virtual environment:
   ```
   pipenv shell
   ```

2. Start the server:
   ```
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## API Documentation

After starting the server, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

- `POST /debate/start` - Start a new philosophical debate
- `GET /debate/{debate_id}` - Get a debate by ID
- `GET /debate/{debate_id}/messages` - Get all messages for a debate
- `GET /quiz/generate/{debate_id}` - Generate a quiz for a completed debate
- `POST /quiz/submit` - Submit quiz answers and get results 