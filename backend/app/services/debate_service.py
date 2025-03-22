import random
import os
import anthropic
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.debate import Debate, Message
from app.schemas.schemas import DebateCreate
import asyncio

# Load environment variables
load_dotenv()

# Configure Anthropic client
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Define thinkers for each position
DUALIST_THINKERS = [
    {
        "name": "René Descartes",
        "position": "Dualist",
        "description": "Argues that the mind is an independently existing substance - the mental does not have extension in space, and the material cannot think."
    },
    {
        "name": "Nicholas Malebranche",
        "position": "Dualist",
        "description": "Argued that a material basis of interaction between the material and immaterial is impossible, and that the interactions were really caused by the intervention of God on each individual occasion."
    }
]

MONIST_THINKERS = [
    {
        "name": "George Berkeley",
        "position": "Monist",
        "description": "Argued that the mind is all that exists (the only existing substance is mental), and that the external world is either mental itself, or an illusion created by the mind."
    },
    {
        "name": "Baruch Spinoza",
        "position": "Monist",
        "description": "Argued that existence consists of one kind of primal substance, which in itself is neither mental nor physical, but is capable of mental and physical aspects or attributes."
    }
]

async def create_debate(db: Session, debate_create: DebateCreate):
    """Create a new debate and start generating responses asynchronously."""
    # Create new debate in the database
    db_debate = Debate(
        topic=debate_create.topic,
        question=debate_create.question
    )
    db.add(db_debate)
    db.commit()
    db.refresh(db_debate)
    
    # Select two thinkers (one from each position)
    dualist = random.choice(DUALIST_THINKERS)
    monist = random.choice(MONIST_THINKERS)
    
    # Start generating debate asynchronously
    asyncio.create_task(generate_debate_messages(db, db_debate.id, dualist, monist, debate_create.question))
    
    return db_debate

async def generate_debate_messages(db: Session, debate_id: int, dualist: dict, monist: dict, question: str):
    """Generate debate messages using Anthropic API and save to database."""
    thinkers = [dualist, monist]
    
    # Define the number of exchanges (4 from each thinker)
    total_messages = 8
    
    for sequence in range(total_messages):
        # Alternate between thinkers
        current_thinker = thinkers[sequence % 2]
        
        # Get previous messages for context
        previous_messages = []
        if sequence > 0:
            db_messages = db.query(Message).filter(
                Message.debate_id == debate_id,
                Message.sequence < sequence
            ).order_by(Message.sequence).all()
            
            for msg in db_messages:
                previous_messages.append(f"{msg.thinker_name} ({msg.thinker_position}): {msg.content}")
        
        # Construct the context for the AI
        context = f"""
        You are simulating a philosophical debate between two thinkers on the topic of Dualism vs. Monism.
        
        The question being debated is: "{question}"
        
        You are responding as {current_thinker['name']}, who is a {current_thinker['position']}.
        {current_thinker['name']} {current_thinker['description']}
        
        Write a response that:
        1. Is faithful to {current_thinker['name']}'s philosophical position
        2. Uses terminology and arguments that this philosopher would use
        3. Directly addresses the question and previous points in the debate
        4. Is about 3-5 sentences long
        5. Is written in the style of the philosopher

        Pretend you are each thinker in the debate. This means you won't introduce your response or introduce yourself as an AI. You are legitimately the philosopher responding to the question.

        Previous exchanges:
        {chr(10).join(previous_messages)}
        """
        
        # Generate response with Anthropic
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            temperature=0.7,
            system=context,
            messages=[
                {"role": "user", "content": f"Respond as {current_thinker['name']} to the question and previous exchanges."}
            ]
        )
        
        # Extract the content
        message_content = response.content[0].text
        
        # Create message in database
        db_message = Message(
            debate_id=debate_id,
            thinker_name=current_thinker['name'],
            thinker_position=current_thinker['position'],
            content=message_content,
            sequence=sequence
        )
        
        # Add to database and commit
        db_session = Session(bind=db.get_bind())
        db_session.add(db_message)
        db_session.commit()
        db_session.close()
        
        # Pause between generating messages to simulate real-time debate
        await asyncio.sleep(5)
    
    # Mark debate as completed
    db_session = Session(bind=db.get_bind())
    db_debate = db_session.query(Debate).filter(Debate.id == debate_id).first()
    db_debate.completed = True
    db_session.commit()
    db_session.close()

def get_debate(db: Session, debate_id: int):
    """Retrieve a debate with all its messages."""
    return db.query(Debate).filter(Debate.id == debate_id).first() 