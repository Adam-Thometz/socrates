from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.schemas import QuizResponse, QuizResultResponse, QuizSubmit
from services.quiz_service import generate_quiz, submit_quiz
from models.quiz import Quiz, QuizQuestion

router = APIRouter()

@router.get("/generate/{debate_id}", response_model=QuizResponse)
def create_quiz_for_debate(debate_id: int, db: Session = Depends(get_db)):
    """Generate a quiz for a completed debate."""
    quiz = generate_quiz(db, debate_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Debate not found or not completed yet")
    
    questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz.id).all()
    quiz.questions = questions
    
    return quiz

@router.post("/submit", response_model=QuizResultResponse)
def submit_quiz_answers(quiz_submit: QuizSubmit, db: Session = Depends(get_db)):
    """Submit quiz answers and get results."""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_submit.debate_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    result = submit_quiz(db, quiz.id, quiz_submit.answers)
    if result is None:
        raise HTTPException(status_code=404, detail="Failed to submit quiz")
    
    return result 