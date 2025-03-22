export interface DebateRequest {
  topic: string;
  question: string;
}

export interface QuizSubmitRequest {
  debate_id: number;
  answers: string[];
} 