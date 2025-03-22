import { Debate, DebateRequest, Quiz, QuizSubmitRequest, QuizResult } from '../types';

const API_URL = 'http://localhost:8000';

/**
 * API service for interacting with the backend
 */
export const api = {
  /**
   * Start a new debate
   */
  startDebate: async (requestData: DebateRequest): Promise<Debate> => {
    const response = await fetch(`${API_URL}/debate/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to start debate');
    }

    const data = await response.json();
    
    return data;
  },
  
  /**
   * Get a debate by ID
   */
  getDebate: async (debateId: number): Promise<Debate> => {
    const response = await fetch(`${API_URL}/debate/${debateId}`);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to get debate');
    }
    
    const data = await response.json();
    
    return data;
  },
  
  /**
   * Generate a quiz for a debate
   */
  generateQuiz: async (debateId: number): Promise<Quiz> => {
    const response = await fetch(`${API_URL}/quiz/generate/${debateId}`);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to generate quiz');
    }
    
    const data = await response.json();
    
    return data;
  },
  
  /**
   * Submit quiz answers
   */
  submitQuiz: async (requestData: QuizSubmitRequest): Promise<QuizResult> => {
    const response = await fetch(`${API_URL}/quiz/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to submit quiz');
    }
    
    const data = await response.json();
    
    return data;
  }
}; 