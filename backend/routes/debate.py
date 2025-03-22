from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.schemas import DebateCreate, DebateResponse
from services.debate_service import create_debate, get_debate

router = APIRouter()

@router.post("/start", response_model=DebateResponse)
async def start_debate(debate_create: DebateCreate, db: Session = Depends(get_db)):
    """Start a new debate on the specified topic with the given question."""
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
