// src/App.js
import React from 'react';
import CompanyList from './components/CompanyList.jsx';
import PrepPlanGenerator from './components/PrepPlanGenerator.jsx';
import MockInterviewSimulator from './components/MockInterviewSimulator.jsx';
import './App.css'; // Your main app CSS
import { useState } from 'react';

function App() {
  const [activeModule, setActiveModule] = useState('companies'); // 'companies', 'prep_plan', 'mock_interviews'

  const renderModule = () => {
      switch(activeModule) {
          case 'companies':
              return <CompanyList />;
          case 'prep_plan':
              return <PrepPlanGenerator />;
          case 'mock_interviews':
              return <MockInterviewSimulator />; 
          default:
              return <CompanyList />;
      }
  }
  return (
    <div className="App">
      <header className="App-header">
        <nav>
          <button onClick={() => setActiveModule('companies')}>Company Drives</button>
          <button onClick={() => setActiveModule('prep_plan')}>Preparation Plan</button>
          <button onClick={() => setActiveModule('mock_interviews')}>Mock Interviews</button>
        </nav>
        <h1>Connect & Conquer</h1>
      </header>
      <main>
        {renderModule()}
        {/* <CompanyList /> */}
      </main>
    </div>
  );
}

export default App;