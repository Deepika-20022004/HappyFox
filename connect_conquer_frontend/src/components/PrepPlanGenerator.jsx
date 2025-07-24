import React, { useState } from 'react';
import './PrepPlanGenerator.css';

function PrepPlanGenerator() {
    const [academicDetails, setAcademicDetails] = useState('');
    const [preferredRole, setPreferredRole] = useState('');
    const [prepPlan, setPrepPlan] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setPrepPlan(null);
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/api/generate_prep_plan/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    academic_course_details: academicDetails,
                    preferred_role: preferredRole,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setPrepPlan(data);
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="prep-plan-container">
            <h1>Generate Your Personalized Preparation Plan</h1>
            <form onSubmit={handleSubmit} className="prep-form">
                <div className="form-group">
                    <label htmlFor="academicDetails">Your Academic Course Details:</label>
                    <textarea
                        id="academicDetails"
                        value={academicDetails}
                        onChange={(e) => setAcademicDetails(e.target.value)}
                        placeholder="e.g., 'Currently in 3rd year CS, studying Databases and OS, finished DSA.'"
                        rows="4"
                        required
                    ></textarea>
                </div>
                <div className="form-group">
                    <label htmlFor="preferredRole">Preferred Role:</label>
                    <input
                        type="text"
                        id="preferredRole"
                        value={preferredRole}
                        onChange={(e) => setPreferredRole(e.target.value)}
                        placeholder="e.g., 'Software Engineer', 'Data Analyst'"
                        required
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Generating...' : 'Generate Plan'}
                </button>
            </form>

            {error && <div className="error-message">Error: {error}</div>}

            {prepPlan && (
                <div className="prep-plan-output">
                    <h2>Your Personalized Plan for {prepPlan.role}</h2>
                    <p className="academic-context-summary">
                        **Based on your input:** {prepPlan.academic_context || 'N/A'}
                    </p>

                    <h3>Core Skills to Focus On:</h3>
                    {prepPlan.plan_details.core_skills && prepPlan.plan_details.core_skills.length > 0 ? (
                        prepPlan.plan_details.core_skills.map((skill, index) => (
                            <div key={index} className="skill-section">
                                <h4>{skill.name}</h4>
                                {skill.topics && skill.topics.length > 0 ? (
                                    <ul>
                                        {skill.topics.map((topic, tIndex) => (
                                            <li key={tIndex}>
                                                <strong>{topic.name}:</strong>
                                                {topic.resources && topic.resources.length > 0 ? (
                                                    <ul className="resource-list">
                                                        {topic.resources.map((res, rIndex) => (
                                                            <li key={rIndex}>
                                                                <a href={res.url} target="_blank" rel="noopener noreferrer">
                                                                    {res.title} ({res.type})
                                                                </a>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                ) : (
                                                    <p>No specific resources found for this topic yet. Check discussions!</p>
                                                )}
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <p>No specific topics found for this skill yet. Keep an eye on updates!</p>
                                )}
                            </div>
                        ))
                    ) : (
                        <p>No specific core skills generated for this role. Try a more common role.</p>
                    )}

                    <h3>Recommendations:</h3>
                    {prepPlan.recommendations ? (
                        <ul>
                            {Object.entries(prepPlan.recommendations).map(([key, value], index) => (
                                <li key={index}>
                                    <strong>{key.replace(/_/g, ' ').toUpperCase()}:</strong> {Array.isArray(value) ? value.join('; ') : value}
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>No specific recommendations generated at this time.</p>
                    )}
                </div>
            )}
        </div>
    );
}

export default PrepPlanGenerator;