import random
import os
import anthropic
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models.debate import Debate, Message
from schemas.schemas import DebateCreate
import asyncio

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

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

HISTORICAL_CONTEXT = {
    "René Descartes": "17th century philosopher writing during the Scientific Revolution, developing his ideas in response to skepticism and mechanistic worldviews of his time.",
    "Nicholas Malebranche": "17th century French priest and rationalist philosopher, heavily influenced by Descartes but developed occasionalism in response to mind-body interaction problems.",
    "George Berkeley": "18th century Irish philosopher responding to Locke and Newton, developing immaterialism partly as a response to skepticism and atheism.",
    "Baruch Spinoza": "17th century Dutch philosopher of Portuguese-Jewish origin, excommunicated for his radical views, developing a unique monist metaphysics partly influenced by Descartes."
}

async def create_debate(db: Session, debate_create: DebateCreate):
    """Create a new debate and start generating responses asynchronously."""
    db_debate = Debate(
        topic=debate_create.topic,
        question=debate_create.question
    )
    db.add(db_debate)
    db.commit()
    db.refresh(db_debate)
    
    dualist = random.choice(DUALIST_THINKERS)
    monist = random.choice(MONIST_THINKERS)
    
    asyncio.create_task(generate_debate_messages(db, db_debate.id, dualist, monist, debate_create.question))
    
    return db_debate

def determine_next_thinker(thinkers: list, key_points: list, sequence: int):
    """Determine which thinker should respond next based on the sequence number and key points."""
    if sequence > 2 and key_points and random.random() < 0.3:
        return thinkers[0] if key_points[-1]["thinker"] == thinkers[1]["name"] else thinkers[1]
    else:
        return thinkers[sequence % 2]

async def generate_debate_messages(db: Session, debate_id: int, dualist: dict, monist: dict, question: str):
    """Generate debate messages using Anthropic API and save to database."""
    thinkers = [dualist, monist]
    random.shuffle(thinkers)
    
    total_messages = 8

    key_points = []
    
    for sequence in range(total_messages):
        current_thinker = determine_next_thinker(thinkers, key_points, sequence)
        
        # Get previous messages for context
        previous_messages = []
        if sequence > 0:
            db_messages = db.query(Message).filter(
                Message.debate_id == debate_id,
                Message.sequence < sequence
            ).order_by(Message.sequence).all()
            
            for msg in db_messages:
                previous_messages.append(f"{msg.thinker_name} ({msg.thinker_position}): {msg.content}")
        
        context = f"""
        You are simulating a philosophical debate between two thinkers on the topic of Dualism vs. Monism.
        
        The question being debated is: "{question}"
        
        You are responding as {current_thinker['name']}, who is a {current_thinker['position']}.
        {current_thinker['name']} {current_thinker['description']}

        Historical context: {HISTORICAL_CONTEXT[current_thinker['name']]}
        
        Write a response that:
        1. Is faithful to {current_thinker['name']}'s philosophical position
        2. Uses terminology and arguments that this philosopher would use but is not too technical
        3. Directly addresses the question and previous points in the debate
        4. Is about 3-5 sentences long,
        5. Is written in the style of the philosopher, including their characteristic rhetorical approaches
        6. References specific works or arguments from their actual philosophical corpus when relevant
        7. Use the Socratic style of dialogue found in Plato's works.

        Restrictions:
        - Phrases that describe how the philosopher is speaking are not allowed. No *speaks in a measured, philosophical tone* or anything like that.
        - Do NOT introduce your response or introduce yourself as an AI. You are legitimately the philosopher responding to the question.
        - Avoid anachronistic references to concepts or terminology that wouldn't have been available to the philosopher.
        - Do NOT go over the sentence limit. The responses should be digestable to beginners.

        Previous exchanges:
        {chr(10).join(previous_messages)}
        """
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            temperature=0.7,
            system=context,
            messages=[
                {"role": "user", "content": f"Respond as {current_thinker['name']} to the question and previous exchanges."}
            ]
        )
        
        message_content = response.content[0].text

        # Analyze response for key points that might deserve follow-up
        if sequence > 0:
            # Simple logic to identify potentially important claims
            if "essence" in message_content or "substance" in message_content or "fundamental" in message_content:
                key_points.append({
                    "sequence": sequence,
                    "thinker": current_thinker['name'],
                    "point": message_content[:100]
                })
        
        db_message = Message(
            debate_id=debate_id,
            thinker_name=current_thinker['name'],
            thinker_position=current_thinker['position'],
            content=message_content,
            sequence=sequence
        )
        
        db_session = Session(bind=db.get_bind())
        db_session.add(db_message)
        db_session.commit()
        db_session.close()
        
        # Pause between generating messages to simulate real-time debate
        await asyncio.sleep(random.uniform(4, 8))
    
    db_session = Session(bind=db.get_bind())
    db_debate = db_session.query(Debate).filter(Debate.id == debate_id).first()
    db_debate.completed = True
    db_session.commit()
    db_session.close()

def get_debate(db: Session, debate_id: int):
    """Retrieve a debate with all its messages."""
    return db.query(Debate).filter(Debate.id == debate_id).first() 