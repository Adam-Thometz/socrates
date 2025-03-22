import { create } from 'zustand';
import { 
  AppStage, 
  Debate, 
  Quiz, 
  QuizResult, 
  DebateRequest,
  QuizSubmitRequest
} from '../types';
import { api } from '../services/api';

interface AppState {
  // App state
  stage: AppStage;
  setStage: (stage: AppStage) => void;
  
  // Debate data
  selectedTopic: string;
  setSelectedTopic: (topic: string) => void;
  
  userQuestion: string;
  setUserQuestion: (question: string) => void;
  
  currentDebate: Debate | null;
  setCurrentDebate: (debate: Debate | null) => void;
  
  // Quiz data
  currentQuiz: Quiz | null;
  setCurrentQuiz: (quiz: Quiz | null) => void;
  
  quizAnswers: string[];
  setQuizAnswers: (answers: string[]) => void;
  updateQuizAnswer: (index: number, answer: string) => void;
  
  quizResult: QuizResult | null;
  setQuizResult: (result: QuizResult | null) => void;
  
  // Loading state
  isLoading: boolean;
  setIsLoading: (isLoading: boolean) => void;
  
  // Error state
  error: string | null;
  setError: (error: string | null) => void;
  
  // API interactions
  startDebate: () => Promise<void>;
  pollDebateMessages: () => Promise<(() => void) | undefined>;
  generateQuiz: () => Promise<void>;
  submitQuiz: () => Promise<void>;
  
  // Utility functions
  reset: () => void;
}

export const useStore = create<AppState>((set, get) => ({
  // Initial state
  stage: AppStage.TopicSelection,
  setStage: (stage: AppStage) => set({ stage }),
  
  selectedTopic: 'Dualism vs. Monism',
  setSelectedTopic: (topic: string) => set({ selectedTopic: topic }),
  
  userQuestion: '',
  setUserQuestion: (question: string) => set({ userQuestion: question }),
  
  currentDebate: null,
  setCurrentDebate: (debate: Debate | null) => set({ currentDebate: debate }),
  
  currentQuiz: null,
  setCurrentQuiz: (quiz: Quiz | null) => set({ currentQuiz: quiz }),
  
  quizAnswers: [],
  setQuizAnswers: (answers: string[]) => set({ quizAnswers: answers }),
  updateQuizAnswer: (index: number, answer: string) => {
    const currentAnswers = [...get().quizAnswers];
    currentAnswers[index] = answer;
    set({ quizAnswers: currentAnswers });
  },
  
  quizResult: null,
  setQuizResult: (result: QuizResult | null) => set({ quizResult: result }),
  
  isLoading: false,
  setIsLoading: (isLoading: boolean) => set({ isLoading }),
  
  error: null,
  setError: (error: string | null) => set({ error }),
  
  // API interactions
  startDebate: async () => {
    const { selectedTopic, userQuestion } = get();
    set({ isLoading: true, error: null });
    
    try {
      const requestData: DebateRequest = {
        topic: selectedTopic,
        question: userQuestion
      };
      
      const debate = await api.startDebate(requestData);
      set({ currentDebate: debate, stage: AppStage.Debate });
      
      // Start polling for new messages
      get().pollDebateMessages();
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'An unknown error occurred' });
    } finally {
      set({ isLoading: false });
    }
  },
  
  pollDebateMessages: async () => {
    const { currentDebate } = get();
    if (!currentDebate) return;
    
    const pollInterval = setInterval(async () => {
      try {
        const updatedDebate = await api.getDebate(currentDebate.id);
        set({ currentDebate: updatedDebate });
        
        // If debate is completed, stop polling and move to quiz
        if (updatedDebate.completed && updatedDebate.messages.length === 8) {
          clearInterval(pollInterval);
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    }, 3000);
    
    return () => clearInterval(pollInterval);
  },
  
  generateQuiz: async () => {
    const { currentDebate } = get();
    if (!currentDebate) return;
    
    set({ isLoading: true, error: null });
    
    try {
      const quiz = await api.generateQuiz(currentDebate.id);
      
      // Initialize answers array with empty strings
      const emptyAnswers = new Array(quiz.questions.length).fill('');
      
      set({ 
        currentQuiz: quiz, 
        quizAnswers: emptyAnswers,
        stage: AppStage.Quiz 
      });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'An unknown error occurred' });
    } finally {
      set({ isLoading: false });
    }
  },
  
  submitQuiz: async () => {
    const { currentQuiz, quizAnswers } = get();
    if (!currentQuiz) return;
    
    set({ isLoading: true, error: null });
    
    try {
      const requestData: QuizSubmitRequest = {
        debate_id: currentQuiz.id,
        answers: quizAnswers
      };
      
      const result = await api.submitQuiz(requestData);
      set({ quizResult: result, stage: AppStage.Results });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'An unknown error occurred' });
    } finally {
      set({ isLoading: false });
    }
  },
  
  // Reset the app state for a new session
  reset: () => {
    set({
      stage: AppStage.TopicSelection,
      userQuestion: '',
      currentDebate: null,
      currentQuiz: null,
      quizAnswers: [],
      quizResult: null,
      error: null
    });
  }
})); 