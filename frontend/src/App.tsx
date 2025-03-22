import React from 'react';
import { useStore } from './store/useStore';
import { AppStage } from './types';

import {
  TopicSelection,
  QuestionInput,
  Debate,
  Quiz,
  Results
} from './views';

import './App.css';

const App: React.FC = () => {
  const { stage } = useStore();
  
  return (
    <div className="app">
      {stage === AppStage.TopicSelection && <TopicSelection />}
      {stage === AppStage.QuestionInput && <QuestionInput />}
      {stage === AppStage.Debate && <Debate />}
      {stage === AppStage.Quiz && <Quiz />}
      {stage === AppStage.Results && <Results />}
    </div>
  );
};

export default App;
