from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.schemas import DebateCreate, DebateResponse, MessageResponse
from app.services.debate_service import create_debate, get_debate
from app.models.debate import Message

router = APIRouter()

@router.post("/start", response_model=DebateResponse)
async def start_debate(debate_create: DebateCreate, db: Session = Depends(get_db)):
    """Start a new debate on the specified topic with the given question."""
    print("debate_create", debate_create)
    if debate_create.topic != "Dualism vs. Monism":
        raise HTTPException(status_code=400, detail="Only 'Dualism vs. Monism' topic is supported for now.")
    
    # Validate question (basic keyword check for on-topic)
    keywords = ["mind", "body", "substance", "dualism", "monism", "physical", "mental", 
                "material", "immaterial", "consciousness", "reality", "perception"]
    
    if not any(keyword in debate_create.question.lower() for keyword in keywords):
        raise HTTPException(status_code=400, 
                           detail="Question seems off-topic. Please ask a question related to mind-body dualism or monism.")
    
    # Create the debate
    debate = await create_debate(db, debate_create)
    return debate

@router.get("/{debate_id}", response_model=DebateResponse)
def get_debate_by_id(debate_id: int, db: Session = Depends(get_db)):
    """Get a debate by ID, including its messages."""
    debate = get_debate(db, debate_id)
    if debate is None:
        raise HTTPException(status_code=404, detail="Debate not found")
    return debate

@router.get("/{debate_id}/messages", response_model=List[MessageResponse])
def get_debate_messages(debate_id: int, db: Session = Depends(get_db)):
    """Get all messages for a debate, ordered by sequence."""
    messages = db.query(Message).filter(Message.debate_id == debate_id).order_by(Message.sequence).all()
    return messages 