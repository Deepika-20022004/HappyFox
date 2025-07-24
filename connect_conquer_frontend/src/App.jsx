// src/App.jsx

import React, { useState } from 'react';
import CompanyList from './components/CompanyList.jsx';
import PrepPlanGenerator from './components/PrepPlanGenerator.jsx';
import MockInterviewSimulator from './components/MockInterviewSimulator.jsx';
import ResumeChecker from './components/ResumeChecker.jsx';
import './App.css';

// Import icons from the library you just installed
import { FaBuilding, FaListAlt, FaLaptopCode, FaUserTie } from 'react-icons/fa';

function App() {
  const [activeModule, setActiveModule] = useState('companies');

  const renderModule = () => {
      switch(activeModule) {
          case 'companies':
              return <CompanyList />;
          case 'prep_plan':
              return <PrepPlanGenerator />;
          case 'mock_interviews':
              return <MockInterviewSimulator />;
          case 'profile_building':
              return <ResumeChecker />;
          default:
              return <CompanyList />;
      }
  }

  // Helper component for navigation buttons to keep code clean
  const NavButton = ({ moduleName, icon, label }) => (
    <button
      className={activeModule === moduleName ? 'active' : ''}
      onClick={() => setActiveModule(moduleName)}
    >
      {icon}
      <span>{label}</span>
    </button>
  );

  return (
    <div className="App">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>Connect & Conquer</h1>
        </div>
        <nav className="sidebar-nav">
          <NavButton
            moduleName="companies"
            icon={<FaBuilding />}
            label="Company Drives"
          />
          <NavButton
            moduleName="prep_plan"
            icon={<FaListAlt />}
            label="Preparation Plan"
          />
          <NavButton
            moduleName="mock_interviews"
            icon={<FaLaptopCode />}
            label="Mock Interviews"
          />
          <NavButton
            moduleName="profile_building"
            icon={<FaUserTie />}
            label="Profile Building"
          />
        </nav>
      </aside>
      <main className="main-content">
        {renderModule()}
      </main>
    </div>
  );
}

export default App;