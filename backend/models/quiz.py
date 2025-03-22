from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, Boolean, Text, String
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    debate_id = Column(Integer, ForeignKey("debates.id"), unique=True)
    score = Column(Float, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    debate = relationship("Debate", back_populates="quiz")
    questions = relationship("QuizQuestion", back_populates="quiz")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question_text = Column(Text, nullable=False)
    correct_answer = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("QuizOption", back_populates="question")

class QuizOption(Base):
    __tablename__ = "quiz_options"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"))
    option_text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)
    
    # Relationships
    question = relationship("QuizQuestion", back_populates="options") 