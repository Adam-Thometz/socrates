from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import debate, quiz
from database.database import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Socrates API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(debate.router, prefix="/debate", tags=["debate"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Socrates API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 