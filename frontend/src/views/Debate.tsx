import React, { useEffect } from 'react';
import { useStore } from '../store/useStore';
import { groupMessagesByThinker } from '../utils';
import { MessageGroup, DebateStatus } from '../components';
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

  const groupedMessages = groupMessagesByThinker(messages);

  const newQuiz = async () => {
    setIsLoading(true);
    try {
      await generateQuiz();
    } finally {
      setIsLoading(false);
    }
  }
  
  return (
    <div className="debate-container">
      <div className="debate-header">
        <h2>{topic}</h2>
        <h3>Question: {question}</h3>
      </div>
      
      <div className="debate-messages">
        {groupedMessages.map((group, groupIndex) => (
          <MessageGroup key={groupIndex} group={group} />
        ))}
        
        <DebateStatus 
          messages={messages} 
          isLoading={isLoading} 
          handleQuizGeneration={newQuiz} 
        />
      </div>
    </div>
  );
};
