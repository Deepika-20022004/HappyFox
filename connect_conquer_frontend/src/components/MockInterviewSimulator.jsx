import React, { useState, useEffect } from 'react';
import './MockInterviewSimulator.css'; // For styling

function MockInterviewSimulator() {
    const [companies, setCompanies] = useState([]);
    const [selectedCompanyId, setSelectedCompanyId] = useState('');
    const [selectedRole, setSelectedRole] = useState('');
    const [mockQuestions, setMockQuestions] = useState([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [userAnswers, setUserAnswers] = useState({});
    const [interviewStarted, setInterviewStarted] = useState(false);
    const [interviewFinished, setInterviewFinished] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch companies for selection (reusing Module 1's API)
    useEffect(() => {
        const fetchCompaniesForSelection = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/companies/');
                if (!response.ok) throw new Error('Failed to fetch companies.');
                const data = await response.json();
                setCompanies(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchCompaniesForSelection();
    }, []);

    const handleStartInterview = async () => {
        if (!selectedCompanyId || !selectedRole) {
            alert('Please select a company and provide a role.');
            return;
        }
        setLoading(true);
        setError(null);
        setInterviewFinished(false);
        setUserAnswers({});
        setCurrentQuestionIndex(0);

        try {
            const response = await fetch('http://localhost:8000/api/generate_mock_interview/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ company_id: selectedCompanyId, role: selectedRole, num_questions: 5 }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.length === 0) {
                alert('No mock questions available for this company/role combination.');
                setLoading(false);
                return;
            }
            setMockQuestions(data);
            setInterviewStarted(true);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleNextQuestion = () => {
        if (currentQuestionIndex < mockQuestions.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
        } else {
            setInterviewFinished(true);
            setInterviewStarted(false);
        }
    };

    const handleAnswerChange = (e) => {
        setUserAnswers({
            ...userAnswers,
            [mockQuestions[currentQuestionIndex].id]: e.target.value,
        });
    };

    const currentQuestion = mockQuestions[currentQuestionIndex];
    const selectedCompany = companies.find(c => c.id === parseInt(selectedCompanyId));

    if (loading && !interviewStarted) return <div className="loading">Loading companies...</div>;
    if (error) return <div className="error">Error: {error}</div>;

    return (
        <div className="mock-interview-container">
            <h1>Mock Interview Simulator</h1>

            {!interviewStarted && !interviewFinished && (
                <div className="interview-setup">
                    <div className="form-group">
                        <label htmlFor="company-select">Select Company:</label>
                        <select
                            id="company-select"
                            value={selectedCompanyId}
                            onChange={(e) => setSelectedCompanyId(e.target.value)}
                        >
                            <option value="">Select a Company</option>
                            {companies.map((company) => (
                                <option key={company.id} value={company.id}>
                                    {company.company_name}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="form-group">
                        <label htmlFor="role-input">Preferred Role:</label>
                        <input
                            type="text"
                            id="role-input"
                            value={selectedRole}
                            onChange={(e) => setSelectedRole(e.target.value)}
                            placeholder="e.g., 'Software Engineer'"
                        />
                    </div>
                    <button onClick={handleStartInterview} disabled={loading}>
                        {loading ? 'Starting...' : 'Start Mock Interview'}
                    </button>
                </div>
            )}

            {interviewStarted && currentQuestion && (
                <div className="interview-active">
                    <h2>{selectedCompany ? selectedCompany.company_name : 'General'} Interview - {selectedRole}</h2>
                    <div className="question-counter">Question {currentQuestionIndex + 1} of {mockQuestions.length}</div>
                    <div className="question-card">
                        <h3>{currentQuestion.question_text}</h3>
                        <p className="question-meta">Type: {currentQuestion.question_type} | Difficulty: {currentQuestion.difficulty_level}</p>
                        <textarea
                            placeholder="Type your answer here..."
                            value={userAnswers[currentQuestion.id] || ''}
                            onChange={handleAnswerChange}
                            rows="8"
                        ></textarea>
                        <button onClick={handleNextQuestion} className="next-button">
                            {currentQuestionIndex < mockQuestions.length - 1 ? 'Next Question' : 'Finish Interview'}
                        </button>
                    </div>
                </div>
            )}

            {interviewFinished && (
                <div className="interview-results">
                    <h2>Mock Interview Completed!</h2>
                    <p>You've answered all {mockQuestions.length} questions.</p>
                    <h3>Your Answers:</h3>
                    {mockQuestions.map((q, index) => (
                        <div key={q.id} className="answer-review-card">
                            <h4>Question {index + 1}: {q.question_text}</h4>
                            <p><strong>Your Answer:</strong></p>
                            <div className="user-answer-text">{userAnswers[q.id] || "No answer provided."}</div>
                            <p><strong>Sample Answer:</strong></p>
                            <div className="sample-answer-text">{q.sample_answer || "No sample answer available."}</div>
                            <p><strong>Keywords to look for:</strong> <em>{q.expected_answer_keywords || 'N/A'}</em></p>
                            {/* Basic self-assessment or "AI feedback" placeholder */}
                            <div className="feedback-placeholder">
                                **Self-Assessment Tip:** Compare your answer to the sample and check for keywords. Did you cover the main points? Was it clear and concise?
                            </div>
                        </div>
                    ))}
                    <button onClick={() => setInterviewFinished(false) || setInterviewStarted(false)}>Start New Interview</button>
                </div>
            )}
        </div>
    );
}

export default MockInterviewSimulator;