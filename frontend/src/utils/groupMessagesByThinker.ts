import { Message } from "../types";

export const groupMessagesByThinker = (messages: Message[]): Message[][] => {
  const grouped: Message[][] = [];
  let currentGroup: Message[] = [];
  
  messages.forEach((message: Message, index: number) => {
    if (index === 0 || messages[index - 1].thinker_name !== message.thinker_name) {
      if (currentGroup.length > 0) {
        grouped.push(currentGroup);
      }
      currentGroup = [message];
    } else {
      currentGroup.push(message);
    }
  });
  
  if (currentGroup.length > 0) {
    grouped.push(currentGroup);
  }
  
  return grouped;
};