import React from 'react';
import { useStore } from '../store/useStore';
import { AppStage } from '../types';

export const TopicSelection: React.FC = () => {
  const { setStage, selectedTopic, setSelectedTopic } = useStore();

  const handleTopicSelect = () => {
    setStage(AppStage.QuestionInput);
  };

  return (
    <div className="topic-selection">
      <h1>Socrates App</h1>
      <h2>Select a Philosophical Topic</h2>
      
      <div className="topic-card" onClick={handleTopicSelect}>
        <h3>Dualism vs. Monism</h3>
        <p>
          Explore the philosophical debate about mind and body.
          Is the mind separate from the body, or are they one substance?
        </p>
        <button onClick={handleTopicSelect}>Select Topic</button>
      </div>

      <div className="coming-soon">
        <h3>More topics coming soon...</h3>
      </div>
    </div>
  );
};
