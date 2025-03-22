export interface QuizOption {
  id: number;
  option_text: string;
  is_correct: boolean;
}

export interface Question {
  id: number;
  question_text: string;
  correct_answer: string;
  options: QuizOption[];
}

export interface Quiz {
  id: number;
  debate_id: number;
  questions: Question[];
}

export interface QuizResult {
  id: number;
  debate_id: number;
  score: number;
  completed: boolean;
}