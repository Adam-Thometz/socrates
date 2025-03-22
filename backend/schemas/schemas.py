from pydantic import BaseModel
from typing import List
from datetime import datetime

# Base schemas
class MessageBase(BaseModel):
    thinker_name: str
    thinker_position: str
    content: str
    sequence: int

class QuizOptionBase(BaseModel):
    option_text: str
    is_correct: bool

class QuizQuestionBase(BaseModel):
    question_text: str
    correct_answer: str

# Request schemas
class DebateCreate(BaseModel):
    topic: str
    question: str

class QuizSubmit(BaseModel):
    debate_id: int
    answers: List[str]

# Response schemas
class MessageResponse(MessageBase):
    id: int
    debate_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class DebateResponse(BaseModel):
    id: int
    topic: str
    question: str
    created_at: datetime
    completed: bool
    messages: List[MessageResponse] = []
    
    class Config:
        orm_mode = True

class QuizOptionResponse(QuizOptionBase):
    id: int
    
    class Config:
        orm_mode = True

class QuizQuestionResponse(QuizQuestionBase):
    id: int
    options: List[QuizOptionResponse] = []
    
    class Config:
        orm_mode = True

class QuizResponse(BaseModel):
    id: int
    debate_id: int
    questions: List[QuizQuestionResponse] = []
    
    class Config:
        orm_mode = True

class QuizResultResponse(BaseModel):
    id: int
    debate_id: int
    score: float
    completed: bool
    
    class Config:
        orm_mode = True 