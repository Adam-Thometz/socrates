# Socrates App

An interactive philosophical debate application that simulates discussions between famous thinkers on the topic of Dualism vs. Monism and tests the user's understanding through quizzes.

## Project Structure

The project consists of two main parts:

- `frontend/`: React application built with TypeScript, Vite, and Zustand
- `backend/`: FastAPI application with SQLite

## Features

1. **Topic Selection**: Choose a philosophical topic to explore (Dualism vs. Monism)
2. **Question Input**: Ask a philosophical question related to the topic
3. **AI-Generated Debate**: AI simulates a debate between two philosophers with opposing views
4. **Quiz**: Test your understanding with multiple-choice questions about what the thinkers argued
5. **Results**: See your score and get feedback on your understanding

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a `.env` file with the following variables:
   ```
   DATABASE_URL=sqlite:///./socrates.db
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```
   
   Replace `your_anthropic_api_key_here` with your actual Anthropic API key.

3. Activate virtual environment:
   ```
   pipenv shell
   ```

4. Install dependencies with pipenv:
   ```
   pipenv install
   ```

5. Start the server:
   ```
   uvicorn main:app --reload
   ```

The backend API will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`.

## How It Works

1. **Select a Topic**: Currently, only the "Dualism vs. Monism" topic is available.
2. **Enter a Question**: Ask a philosophical question related to mind and body.
3. **Watch the Debate**: The app randomly selects one "dualist" and one "monist" thinker:
   - **Dualists**: René Descartes, Nicholas Malebranche
   - **Monists**: George Berkeley, Baruch Spinoza
4. **Take the Quiz**: Answer multiple-choice questions about what each thinker believes.
5. **View Results**: See your score and feedback.

## Technical Details

### Frontend

- Built with React and TypeScript
- State management with Zustand
- Uses polling mechanism to fetch new debate messages every 3 seconds

### Backend

- Built with FastAPI and SQLAlchemy
- Uses Anthropic's Claude API to generate philosophical responses
- Asynchronously generates debate messages and stores them in a database
- Creates quizzes based on the content of debates

## API Endpoints

- `POST /debate/start` - Start a new philosophical debate
- `GET /debate/{debate_id}` - Get a debate by ID
- `GET /quiz/generate/{debate_id}` - Generate a quiz for a completed debate
- `POST /quiz/submit` - Submit quiz answers and get results 