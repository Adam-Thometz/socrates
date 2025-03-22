import anthropic
import os
import json
import re
from sqlalchemy.orm import Session
from models.debate import Debate
from models.quiz import Quiz, QuizQuestion, QuizOption
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def extract_json_from_response(response: str) -> dict:
    """Extract JSON from the response."""
    json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        json_str = re.search(r'{.*}', response, re.DOTALL).group(0)
    return json.loads(json_str)

def grade_quiz(questions: list, answers: list) -> int:
    """Grade a quiz based on the correct answers."""
    correct_count = 0
    total_questions = len(questions)
    if total_questions == 0:
        return 0
    
    for i, question in enumerate(questions):
        if i < len(answers) and question.correct_answer == answers[i]:
            correct_count += 1
    
    return (correct_count / total_questions) * 100

def generate_quiz(db: Session, debate_id: int):
    """Generate a quiz based on a completed debate."""
    debate = db.query(Debate).filter(Debate.id == debate_id).first()
    if not debate or not debate.completed:
        return None
    
    existing_quiz = db.query(Quiz).filter(Quiz.debate_id == debate_id).first()
    if existing_quiz:
        return existing_quiz
    
    quiz = Quiz(debate_id=debate_id)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    messages = debate.messages
    
    message_texts = [f"{msg.thinker_name} ({msg.thinker_position}): {msg.content}" for msg in messages]
    debate_text = "\n".join(message_texts)
    
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
    
    content = response.content[0].text
    questions_data = extract_json_from_response(content)
    
    for q_data in questions_data["questions"]:
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
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return None
    
    questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).all()
    
    quiz.score = grade_quiz(questions, answers)
    
    quiz.completed = True
    db.commit()
    
    return quiz 