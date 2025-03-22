import { Message } from '../types';

export const MessageGroup: React.FC<{ group: Message[] }> = ({ group }) => {
  const thinker = group[0].thinker_name;
  const position = group[0].thinker_position;
  const isMonist = position === 'Monist';
  
  return (
    <div className={`message-group ${isMonist ? 'monist' : 'dualist'}`}>
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
};