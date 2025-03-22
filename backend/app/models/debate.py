from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class Debate(Base):
    __tablename__ = "debates"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    
    # Relationships
    messages = relationship("Message", back_populates="debate")
    quiz = relationship("Quiz", back_populates="debate", uselist=False)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    debate_id = Column(Integer, ForeignKey("debates.id"))
    thinker_name = Column(String, nullable=False)
    thinker_position = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    sequence = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    debate = relationship("Debate", back_populates="messages")