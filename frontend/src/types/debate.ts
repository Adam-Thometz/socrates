export interface Thinker {
  name: string;
  position: string;
}

export interface Message {
  id: number;
  debate_id: number;
  thinker_name: string;
  thinker_position: string;
  content: string;
  sequence: number;
  created_at: string;
}

export interface Debate {
  id: number;
  topic: string;
  question: string;
  created_at: string;
  completed: boolean;
  messages: Message[];
}