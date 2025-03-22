import React from 'react';
import { useStore } from '../store/useStore';
import { showQuizScore } from '../utils';
export const Results: React.FC = () => {
  const { quizResult, reset } = useStore();

  if (!quizResult) {
    return <div className="loading">Loading results...</div>;
  }

  const { score } = quizResult;
  
  const { feedback, feedbackClass } = showQuizScore(score);

  const handlePlayAgain = () => {
    reset();
  };

  return (
    <div className="results-container">
      <h2>Quiz Results</h2>
      
      <div className={`score-display ${feedbackClass}`}>
        <div className="score-value">{Math.round(score)}%</div>
        <div className="score-label">Score</div>
      </div>
      
      <div className="feedback">
        <p>{feedback}</p>
      </div>
      
      <div className="results-actions">
        <button onClick={handlePlayAgain}>
          Try Another Question
        </button>
      </div>
    </div>
  );
};
