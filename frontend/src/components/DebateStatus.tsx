import { Message } from "../types";

interface DebateStatusProps {
  messages: Message[];
  isLoading: boolean;
  handleQuizGeneration: () => void;
}

export const DebateStatus: React.FC<DebateStatusProps> = ({ messages, isLoading, handleQuizGeneration }) => {
  if (messages.length < 8) {
    return (
      <div className="debate-status">
        {isLoading ? 'Philosophers are thinking...' : 'Waiting for the next response...'}
      </div>
    );
  }
  
  return (
    <div className="debate-complete">
      <p>The debate is complete. Read through the responses and then click Continue to take a quiz on the debate.</p>
      <button 
        className="continue-button"
        onClick={handleQuizGeneration}
        disabled={isLoading}
      >
        {isLoading ? 'Generating quiz...' : 'Continue'}
      </button>
    </div>
  );
};