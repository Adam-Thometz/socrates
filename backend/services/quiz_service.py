import anthropic
import os
import random
from sqlalchemy.orm import Session
from app.models.debate import Debate
from app.models.quiz import Quiz, QuizQuestion, QuizOption
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Anthropic client
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def generate_quiz(db: Session, debate_id: int):
    """Generate a quiz based on a completed debate."""
    # Check if debate exists and is completed
    debate = db.query(Debate).filter(Debate.id == debate_id).first()
    if not debate or not debate.completed:
        return None
    
    # Check if quiz already exists
    existing_quiz = db.query(Quiz).filter(Quiz.debate_id == debate_id).first()
    if existing_quiz:
        return existing_quiz
    
    # Create new quiz
    quiz = Quiz(debate_id=debate_id)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    # Get all debate messages
    messages = debate.messages
    
    # Use Anthropic to generate questions
    message_texts = [f"{msg.thinker_name} ({msg.thinker_position}): {msg.content}" for msg in messages]
    debate_text = "\n".join(message_texts)
    
    # Generate 5 quiz questions
    prompt = f"""
    I'm going to show you a philosophical debate between two thinkers on Dualism vs. Monism. 
    After reading the debate, please create 5 multiple-choice questions testing understanding of what each thinker believes.
    
    The debate:
    {debate_text}
    
    For each question:
    1. Create a question about what one of the thinkers believes or said
    2. Provide 4 possible answers (A, B, C, D)
    3. Indicate which answer is correct
    
    Format your response as a JSON object with this structure:
    {{
        "questions": [
            {{
                "question": "Question text here?",
                "options": [
                    {{ "text": "Option A", "is_correct": false }},
                    {{ "text": "Option B", "is_correct": true }},
                    {{ "text": "Option C", "is_correct": false }},
                    {{ "text": "Option D", "is_correct": false }}
                ]
            }}
        ]
    }}
    
    Please ensure each question has exactly one correct answer.
    """
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0.7,
        system="You are an expert in philosophy and education, creating quiz questions about philosophical debates.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract and parse JSON response
    import json
    import re
    
    # Try to extract JSON from the response
    content = response.content[0].text
    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        json_str = re.search(r'{.*}', content, re.DOTALL).group(0)
    
    questions_data = json.loads(json_str)
    
    # Add questions and options to database
    for q_data in questions_data["questions"]:
        # Create question
        question = QuizQuestion(
            quiz_id=quiz.id,
            question_text=q_data["question"],
            correct_answer=next(opt["text"] for opt in q_data["options"] if opt["is_correct"])
        )
        db.add(question)
        db.commit()
        db.refresh(question)
        
        # Create options
        for opt_data in q_data["options"]:
            option = QuizOption(
                question_id=question.id,
                option_text=opt_data["text"],
                is_correct=opt_data["is_correct"]
            )
            db.add(option)
        
    db.commit()
    
    return quiz

def submit_quiz(db: Session, quiz_id: int, answers: list):
    """Submit quiz answers and calculate score."""
    # Get quiz and questions
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return None
    
    questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).all()
    
    # Calculate score
    correct_count = 0
    total_questions = len(questions)
    
    for i, question in enumerate(questions):
        if i < len(answers) and question.correct_answer == answers[i]:
            correct_count += 1
    
    # Update quiz with score
    if total_questions > 0:
        quiz.score = (correct_count / total_questions) * 100
    else:
        quiz.score = 0
    
    quiz.completed = True
    db.commit()
    
    return quiz 