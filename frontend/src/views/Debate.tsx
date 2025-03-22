import React, { useEffect } from 'react';
import { useStore } from '../store/useStore';
import { Message } from '../types';

export const Debate: React.FC = () => {
  const { currentDebate, pollDebateMessages, isLoading, generateQuiz, setIsLoading } = useStore();
  
  // Start polling for messages when component mounts
  useEffect(() => {
    pollDebateMessages();
  }, [pollDebateMessages]);
  
  if (!currentDebate) {
    return <div className="loading">Loading debate...</div>;
  }
  
  const { topic, question, messages } = currentDebate;

  const groupedMessages: Message[][] = [];
  let currentGroup: Message[] = [];
  
  messages.forEach((message: Message, index: number) => {
    if (index === 0 || messages[index - 1].thinker_name !== message.thinker_name) {
      if (currentGroup.length > 0) {
        groupedMessages.push(currentGroup);
      }
      currentGroup = [message];
    } else {
      currentGroup.push(message);
    }
  });
  
  if (currentGroup.length > 0) {
    groupedMessages.push(currentGroup);
  }

  const newQuiz = async () => {
    setIsLoading(true);
    await generateQuiz();
    setIsLoading(false);
  }
  
  return (
    <div className="debate-container">
      <div className="debate-header">
        <h2>{topic}</h2>
        <h3>Question: {question}</h3>
      </div>
      
      <div className="debate-messages">
        {groupedMessages.map((group, groupIndex) => {
          const thinker = group[0].thinker_name;
          const position = group[0].thinker_position;
          const isMonist = position === 'Monist';
          
          return (
            <div 
              key={groupIndex} 
              className={`message-group ${isMonist ? 'monist' : 'dualist'}`}
            >
              <div className="thinker-info">
                <strong>{thinker}</strong>
                <span className="position">({position})</span>
              </div>
              
              {group.map((message, messageIndex) => (
                <div key={messageIndex} className="message">
                  {message.content}
                </div>
              ))}
            </div>
          );
        })}
        
        {messages.length < 8 && (
          <div className="debate-status">
            {isLoading ? 'Philosophers are thinking...' : 'Waiting for the next response...'}
          </div>
        )}

        {messages.length >= 8 && (
          <div className="debate-complete">
            <p>The debate is complete. Read through the responses and then click Continue to take a quiz on the debate.</p>
            <button 
              className="continue-button"
              onClick={newQuiz}
            >
              Continue
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
