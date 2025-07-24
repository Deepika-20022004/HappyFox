// import React, { useState } from 'react';
// import CompanyList from './components/CompanyList.jsx';
// import PrepPlanGenerator from './components/PrepPlanGenerator.jsx';
// import MockInterviewSimulator from './components/MockInterviewSimulator.jsx';
// import ResumeChecker from './components/ResumeChecker.jsx';
// import './App.css';

// // Import icons from the library you just installed
// import { FaBuilding, FaListAlt, FaLaptopCode, FaUserTie } from 'react-icons/fa';

// function App() {
//   const [activeModule, setActiveModule] = useState('companies');

//   const renderModule = () => {
//       switch(activeModule) {
//           case 'companies':
//               return <CompanyList />;
//           case 'prep_plan':
//               return <PrepPlanGenerator />;
//           case 'mock_interviews':
//               return <MockInterviewSimulator />;
//           case 'profile_building':
//               return <ResumeChecker />;
//           default:
//               return <CompanyList />;
//       }
//   }

//   // Helper component for navigation buttons to keep code clean
//   const NavButton = ({ moduleName, icon, label }) => (
//     <button
//       className={activeModule === moduleName ? 'active' : ''}
//       onClick={() => setActiveModule(moduleName)}
//     >
//       {icon}
//       <span>{label}</span>
//     </button>
//   );

//   return (
//     <div className="App">
//       <aside className="sidebar">
//         <div className="sidebar-header">
//           <h1>Connect & Conquer</h1>
//         </div>
//         <nav className="sidebar-nav">
//           <NavButton
//             moduleName="companies"
//             icon={<FaBuilding />}
//             label="Company Drives"
//           />
//           <NavButton
//             moduleName="prep_plan"
//             icon={<FaListAlt />}
//             label="Preparation Plan"
//           />
//           <NavButton
//             moduleName="mock_interviews"
//             icon={<FaLaptopCode />}
//             label="Mock Interviews"
//           />
//           <NavButton
//             moduleName="profile_building"
//             icon={<FaUserTie />}
//             label="Profile Building"
//           />
//         </nav>
//       </aside>
//       <main className="main-content">
//         {renderModule()}
//       </main>
//     </div>
//   );
// }

// export default App;

// src/App.jsx

import React from 'react';
import { Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import './App.css';

// Import Pages and Components
import CompanyList from './components/CompanyList.jsx';
import PrepPlanGenerator from './components/PrepPlanGenerator.jsx';
import MockInterviewSimulator from './components/MockInterviewSimulator.jsx';
import ResumeChecker from './components/ResumeChecker.jsx';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import Header from './components/Header.jsx';
import ExperienceListPage from './pages/ExperienceListPage.jsx';
import ExperienceDetailPage from './pages/ExperienceDetailPage.jsx';
import AddExperiencePage from './pages/AddExperiencePage.jsx';
import PrivateRoute from './utils/PrivateRoute.jsx';


// Import Icons
import { FaBuilding, FaListAlt, FaLaptopCode, FaUserTie, FaPenSquare } from 'react-icons/fa';

function App() {
    const location = useLocation();

    // Helper component for navigation links to keep code clean
    const NavLink = ({ to, icon, label }) => {
        const isActive = location.pathname.startsWith(to);
        return (
            <Link to={to} className={isActive ? 'active' : ''}>
                {icon}
                <span>{label}</span>
            </Link>
        );
    };

    return (
        <div className="App">
            <aside className="sidebar">
                <div className="sidebar-header">
                    <h1>Connect & Conquer</h1>
                </div>
                <nav className="sidebar-nav">
                    <NavLink to="/companies" icon={<FaBuilding />} label="Company Drives" />
                    <NavLink to="/prep-plan" icon={<FaListAlt />} label="Preparation Plan" />
                    <NavLink to="/mock-interviews" icon={<FaLaptopCode />} label="Mock Interviews" />
                    <NavLink to="/profile-builder" icon={<FaUserTie />} label="Profile Building" />
                    <NavLink to="/experiences" icon={<FaPenSquare />} label="Experiences" />
                </nav>
                {/* Move Header to the bottom of the sidebar */}
                <div className="sidebar-footer">
                    <Header />
                </div>
            </aside>
            <main className="main-content">
                    <Routes>
                        {/* Existing Routes */}
                        <Route path="/companies" element={<CompanyList />} />
                        <Route path="/prep-plan" element={<PrepPlanGenerator />} />
                        <Route path="/mock-interviews" element={<MockInterviewSimulator />} />
                        <Route path="/profile-builder" element={<ResumeChecker />} />
                        <Route path="/login" element={<LoginPage />} />
                        <Route path="/register" element={<RegisterPage />} />
                        
                        {/* Experience Routes */}
                        <Route path="/experiences" element={<ExperienceListPage />} />
                        <Route path="/experiences/:id" element={<ExperienceDetailPage />} />
                        
                        {/* Protected Route for adding an experience */}
                        <Route element={<PrivateRoute />}>
                            <Route path="/add-experience" element={<AddExperiencePage />} />
                        </Route>
                        
                        {/* Add a default route to redirect to /companies */}
                        <Route path="/" element={<Navigate to="/companies" replace />} />
                    </Routes>
            </main>
        </div>
    );
}

export default App;