import React, { useState } from 'react';
import { useStore } from '../store/useStore';
import { AppStage } from '../types';
import { validateQuestion } from '../utils/validateQuestion';

export const QuestionInput: React.FC = () => {
  const { 
    selectedTopic, 
    userQuestion, 
    setUserQuestion, 
    startDebate,
    setStage,
    isLoading,
    error
  } = useStore();
  
  const [validation, setValidation] = useState<string | null>(null);

  const handleQuestionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setUserQuestion(e.target.value);
    setValidation(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const validationResults = validateQuestion(userQuestion);

    if (!validationResults.isValid) {
      setValidation(validationResults.errorMessage || "Invalid question.");
    } else {
      startDebate();
    }
  };
  
  const handleBack = () => {
    setStage(AppStage.TopicSelection);
  };
  
  // Provide some preset questions as examples
  const presetQuestions = [
    "How does consciousness relate to the physical body?",
    "Is the mind separate from the body?",
    "How can mental states affect physical states if they are different substances?"
  ];
  
  const setPresetQuestion = (question: string) => {
    setUserQuestion(question);
    setValidation(null);
  };

  return (
    <div className="question-input">
      <h2>Ask a Question about {selectedTopic}</h2>
      
      <form onSubmit={handleSubmit}>
        <textarea 
          value={userQuestion}
          onChange={handleQuestionChange}
          placeholder="Enter your philosophical question here..."
          rows={4}
        />
        
        {validation && <div className="validation-error">{validation}</div>}
        {error && <div className="error">{error}</div>}
        
        <div className="button-group">
          <button type="button" onClick={handleBack}>Back</button>
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Starting Debate...' : 'Start Debate'}
          </button>
        </div>
      </form>
      
      <div className="preset-questions">
        <h3>Or try one of these questions:</h3>
        <ul>
          {presetQuestions.map((question, index) => (
            <li key={index} onClick={() => setPresetQuestion(question)}>
              {question}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
