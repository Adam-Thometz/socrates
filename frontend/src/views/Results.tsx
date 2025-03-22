import React from 'react';
import { useStore } from '../store/useStore';

export const Results: React.FC = () => {
  const { quizResult, reset } = useStore();

  if (!quizResult) {
    return <div className="loading">Loading results...</div>;
  }

  const { score } = quizResult;
  
  // Define feedback based on score
  let feedback = '';
  let feedbackClass = '';
  
  if (score >= 90) {
    feedback = "Excellent! You have a deep understanding of these philosophical positions.";
    feedbackClass = 'excellent';
  } else if (score >= 70) {
    feedback = "Good job! You grasp the main concepts well.";
    feedbackClass = 'good';
  } else if (score >= 50) {
    feedback = "Not bad. You understand some key differences in these philosophical views.";
    feedbackClass = 'average';
  } else {
    feedback = "Keep studying! These philosophical concepts can be challenging.";
    feedbackClass = 'needs-work';
  }

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
