// For integrating AI

import React, { useState } from 'react';
import axios from 'axios'; // Using axios for cleaner API calls
import './css/PrepPlanGenerator.css'; // Assuming you have this CSS file

// A new component to display each week's plan clearly
const PlanWeekCard = ({ week, topic_focus, learning_goals, suggested_resources }) => {
    return (
        <div className="plan-week-card">
            <h3>{week}: {topic_focus}</h3>
            <h4>Learning Goals:</h4>
            <p>{learning_goals}</p>
            <h4>Suggested Resources:</h4>
            <p>{suggested_resources}</p>
        </div>
    );
};

function PrepPlanGenerator() {
    // States for the new, more detailed form
    const [courseDetails, setCourseDetails] = useState('');
    const [preferredRole, setPreferredRole] = useState('');
    const [currentSkills, setCurrentSkills] = useState('');
    const [timeframe, setTimeframe] = useState(8); // Default 8 weeks

    // States for API handling and response
    const [weeklyPlan, setWeeklyPlan] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setWeeklyPlan(null);
        setError(null);

        // Updated request body with all the new details
        const requestData = {
            course_details: courseDetails,
            preferred_role: preferredRole,
            current_skills: currentSkills,
            timeframe_weeks: timeframe,
        };

        try {
            // Updated API endpoint
            const response = await axios.post('http://localhost:8000/api/generate_prep_plan/', requestData);
            setWeeklyPlan(response.data.weekly_plan); // Access the 'weekly_plan' key
        } catch (err) {
            const errorMessage = err.response?.data?.error || 'Failed to generate plan. The AI server may be busy.';
            setError(errorMessage);
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="prep-plan-container">
            <h1>Generate Your Personalized Preparation Plan</h1>
            <p>Fill in your details to get a custom, AI-powered study roadmap.</p>
            <form onSubmit={handleSubmit} className="prep-form">
                <div className="form-group">
                    <label htmlFor="courseDetails">Your Course & Year:</label>
                    <input
                        id="courseDetails"
                        type="text"
                        value={courseDetails}
                        onChange={(e) => setCourseDetails(e.target.value)}
                        placeholder="e.g., B.Tech CSE, 3rd Year"
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="preferredRole">Preferred Role:</label>
                    <input
                        id="preferredRole"
                        type="text"
                        value={preferredRole}
                        onChange={(e) => setPreferredRole(e.target.value)}
                        placeholder="e.g., Backend Developer"
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="currentSkills">Your Strengths & Known Skills:</label>
                    <textarea
                        id="currentSkills"
                        value={currentSkills}
                        onChange={(e) => setCurrentSkills(e.target.value)}
                        placeholder="e.g., Python, C++, DSA Basics, SQL"
                        rows="3"
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="timeframe">Preparation Timeframe: {timeframe} weeks</label>
                    <input
                        id="timeframe"
                        type="range"
                        min="2"
                        max="16"
                        value={timeframe}
                        onChange={(e) => setTimeframe(parseInt(e.target.value))}
                        className="slider"
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Generating Plan...' : 'Generate My Plan'}
                </button>
            </form>

            {error && <div className="error-message">Error: {error}</div>}

            {weeklyPlan && (
                <div className="prep-plan-output">
                    <h2>Your Personal Roadmap</h2>
                    {weeklyPlan.map((weekData, index) => (
                        <PlanWeekCard key={index} {...weekData} />
                    ))}
                </div>
            )}
        </div>
    );
}

export default PrepPlanGenerator;


// import React, { useState } from 'react';
// import './PrepPlanGenerator.css';

// function PrepPlanGenerator() {
//     const [academicDetails, setAcademicDetails] = useState('');
//     const [preferredRole, setPreferredRole] = useState('');
//     const [prepPlan, setPrepPlan] = useState(null);
//     const [loading, setLoading] = useState(false);
//     const [error, setError] = useState(null);

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setLoading(true);
//         setPrepPlan(null);
//         setError(null);

//         try {
//             const response = await fetch('http://localhost:8000/api/generate_prep_plan/', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({
//                     academic_course_details: academicDetails,
//                     preferred_role: preferredRole,
//                 }),
//             });

//             if (!response.ok) {
//                 const errorData = await response.json();
//                 throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
//             }

//             const data = await response.json();
//             setPrepPlan(data);
//         } catch (e) {
//             setError(e.message);
//         } finally {
//             setLoading(false);
//         }
//     };

//     return (
//         <div className="prep-plan-container">
//             <h1>Generate Your Personalized Preparation Plan</h1>
//             <form onSubmit={handleSubmit} className="prep-form">
//                 <div className="form-group">
//                     <label htmlFor="academicDetails">Your Academic Course Details:</label>
//                     <textarea
//                         id="academicDetails"
//                         value={academicDetails}
//                         onChange={(e) => setAcademicDetails(e.target.value)}
//                         placeholder="e.g., 'Currently in 3rd year CS, studying Databases and OS, finished DSA.'"
//                         rows="4"
//                         required
//                     ></textarea>
//                 </div>
//                 <div className="form-group">
//                     <label htmlFor="preferredRole">Preferred Role:</label>
//                     <input
//                         type="text"
//                         id="preferredRole"
//                         value={preferredRole}
//                         onChange={(e) => setPreferredRole(e.target.value)}
//                         placeholder="e.g., 'Software Engineer', 'Data Analyst'"
//                         required
//                     />
//                 </div>
//                 <button type="submit" disabled={loading}>
//                     {loading ? 'Generating...' : 'Generate Plan'}
//                 </button>
//             </form>

//             {error && <div className="error-message">Error: {error}</div>}

//             {prepPlan && (
//                 <div className="prep-plan-output">
//                     <h2>Your Personalized Plan for {prepPlan.role}</h2>
//                     <p className="academic-context-summary">
//                         **Based on your input:** {prepPlan.academic_context || 'N/A'}
//                     </p>

//                     <h3>Core Skills to Focus On:</h3>
//                     {prepPlan.plan_details.core_skills && prepPlan.plan_details.core_skills.length > 0 ? (
//                         prepPlan.plan_details.core_skills.map((skill, index) => (
//                             <div key={index} className="skill-section">
//                                 <h4>{skill.name}</h4>
//                                 {skill.topics && skill.topics.length > 0 ? (
//                                     <ul>
//                                         {skill.topics.map((topic, tIndex) => (
//                                             <li key={tIndex}>
//                                                 <strong>{topic.name}:</strong>
//                                                 {topic.resources && topic.resources.length > 0 ? (
//                                                     <ul className="resource-list">
//                                                         {topic.resources.map((res, rIndex) => (
//                                                             <li key={rIndex}>
//                                                                 <a href={res.url} target="_blank" rel="noopener noreferrer">
//                                                                     {res.title} ({res.type})
//                                                                 </a>
//                                                             </li>
//                                                         ))}
//                                                     </ul>
//                                                 ) : (
//                                                     <p>No specific resources found for this topic yet. Check discussions!</p>
//                                                 )}
//                                             </li>
//                                         ))}
//                                     </ul>
//                                 ) : (
//                                     <p>No specific topics found for this skill yet. Keep an eye on updates!</p>
//                                 )}
//                             </div>
//                         ))
//                     ) : (
//                         <p>No specific core skills generated for this role. Try a more common role.</p>
//                     )}

//                     <h3>Recommendations:</h3>
//                     {prepPlan.recommendations ? (
//                         <ul>
//                             {Object.entries(prepPlan.recommendations).map(([key, value], index) => (
//                                 <li key={index}>
//                                     <strong>{key.replace(/_/g, ' ').toUpperCase()}:</strong> {Array.isArray(value) ? value.join('; ') : value}
//                                 </li>
//                             ))}
//                         </ul>
//                     ) : (
//                         <p>No specific recommendations generated at this time.</p>
//                     )}
//                 </div>
//             )}
//         </div>
//     );
// }

// export default PrepPlanGenerator;