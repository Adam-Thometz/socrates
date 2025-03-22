import React, { useEffect } from 'react';
import { useStore } from '../store/useStore';
import { Question } from '../types';
import { QuizQuestion } from '../components';

export const Quiz: React.FC = () => {
  const { 
    currentQuiz, 
    generateQuiz, 
    quizAnswers, 
    updateQuizAnswer,
    submitQuiz,
    isLoading,
    error
  } = useStore();

  useEffect(() => {
    if (!currentQuiz) {
      generateQuiz();
    }
  }, [currentQuiz, generateQuiz]);

  if (!currentQuiz || isLoading) {
    return <div className="loading">Loading quiz questions...</div>;
  }

  const handleAnswerSelect = (questionIndex: number, answer: string) => {
    updateQuizAnswer(questionIndex, answer);
  };

  const handleSubmit = () => {
    const allAnswered = quizAnswers.every((answer: string) => answer !== '');
    
    if (!allAnswered) {
      alert('Please answer all questions before submitting.');
      return;
    }
    
    submitQuiz();
  };

  return (
    <div className="quiz-container">
      <h2>Test Your Understanding</h2>
      <p>Based on the philosophical debate you just witnessed, answer these questions:</p>

      {error && <div className="error">{error}</div>}

      <div className="quiz-questions">
        {currentQuiz.questions.map((question: Question, qIndex: number) => (
          <QuizQuestion 
            key={`question-${qIndex + 1}`} 
            question={question} 
            index={qIndex} 
            handleAnswerSelect={handleAnswerSelect} 
          />
        ))}
      </div>

      <div className="quiz-actions">
        <button 
          onClick={handleSubmit}
          disabled={isLoading || quizAnswers.some((a: string) => a === '')}
        >
          {isLoading ? 'Submitting...' : 'Submit Answers'}
        </button>
      </div>
    </div>
  );
};
