import { useStore } from "../store/useStore";
import { QuizOption, Question } from "../types";

interface QuizQuestionProps {
  question: Question;
  index: number;
  handleAnswerSelect: (index: number, answer: string) => void;
}

export const QuizQuestion: React.FC<QuizQuestionProps> = ({ question, index, handleAnswerSelect }) => {
  const { quizAnswers } = useStore();
  return (
    <div key={`question-${index + 1}`} className="quiz-question">
      <h3>Question {index + 1}</h3>
      <p>{question.question_text}</p>

      <div className="options">
        {question.options.map((option: QuizOption, oIndex: number) => (
          <div 
            key={oIndex} 
            className={`option ${quizAnswers[index] === option.option_text ? 'selected' : ''}`}
            onClick={() => handleAnswerSelect(index, option.option_text)}
          >
            <span className="option-label">{String.fromCharCode(65 + oIndex)}.</span>
            {option.option_text}
          </div>
        ))}
      </div>
    </div>
  );
};