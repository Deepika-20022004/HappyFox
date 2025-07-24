import React, { useState } from 'react';
import axios from 'axios';
import './css/ResumeChecker.css';

function ResumeChecker() {
    const [resumeFile, setResumeFile] = useState(null);
    const [jobDescription, setJobDescription] = useState('');
    const [analysisResult, setAnalysisResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setResumeFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!resumeFile || !jobDescription) {
            setError('Please provide both a resume and a job description.');
            return;
        }

        setLoading(true);
        setError(null);
        setAnalysisResult(null);

        const formData = new FormData();
        // IMPORTANT: Update field names to match the backend (Code 2)
        formData.append('resume_file', resumeFile);
        formData.append('job_description_text', jobDescription);

        try {
            const response = await axios.post('http://localhost:8000/api/profile/check_resume/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setAnalysisResult(response.data);
        } catch (err) {
            const errorMessage = err.response?.data?.error || 'Failed to analyze resume. The server might be busy or an error occurred.';
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const renderSuggestions = (suggestions) => {
        if (!suggestions || suggestions.length === 0) {
            return <p>No specific suggestions provided.</p>;
        }
        return suggestions.map((item, index) => (
            <div key={index} className="suggestion-category">
                <h4>{item.category}</h4>
                <ul>
                    {item.suggestions.map((suggestion, sIndex) => (
                        <li key={sIndex}>{suggestion}</li>
                    ))}
                </ul>
            </div>
        ));
    };

    return (
        <div className="resume-checker-container">
            <h1>AI-Powered Resume Analyzer</h1>
            <p>Upload your resume and paste a job description to get a comprehensive analysis and improvement plan.</p>
            <form onSubmit={handleSubmit} className="resume-form">
                <div className="form-group">
                    <label htmlFor="resumeFile">Upload Your Resume (PDF, DOCX, or TXT):</label>
                    <input
                        id="resumeFile"
                        type="file"
                        accept=".pdf,.docx,.txt"
                        onChange={handleFileChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="jobDescription">Paste Job Description:</label>
                    <textarea
                        id="jobDescription"
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        placeholder="Paste the full job description here..."
                        rows="10"
                        required
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Analyzing...' : 'Analyze My Resume'}
                </button>
            </form>

            {error && <div className="error-message">Error: {error}</div>}

            {analysisResult && (
                <div className="analysis-results">
                    <h2>Analysis Complete</h2>
                    {analysisResult.disclaimer && <p className="disclaimer"><em>{analysisResult.disclaimer}</em></p>}

                    <div className="scores-container">
                        <div className="score-card">
                            <h3>Overall Match</h3>
                            <p>{analysisResult.overall_match_score || 'N/A'}</p>
                        </div>
                        <div className="score-card">
                            <h3>ATS Compatibility</h3>
                            <p>{analysisResult.ats_compatibility_score || 'N/A'}</p>
                        </div>
                    </div>

                    <div className="card">
                        <h3>✅ Resume Strengths</h3>
                        <ul>
                            {analysisResult.resume_strengths?.map((item, i) => <li key={i}>{item}</li>)}
                        </ul>
                    </div>

                    <div className="card">
                        <h3>🎯 Action Items</h3>
                        <ul>
                            {analysisResult.action_items?.map((item, i) => <li key={i}>{item}</li>)}
                        </ul>
                    </div>

                    <div className="card">
                        <h3>💡 Improvement Suggestions</h3>
                        {renderSuggestions(analysisResult.improvement_suggestions)}
                    </div>

                    <div className="keywords-container">
                        <div className="keywords-list found">
                            <h4>Matched Keywords</h4>
                            <ul>
                                {analysisResult.matched_keywords?.map((kw, i) => <li key={i}>{kw}</li>)}
                            </ul>
                        </div>
                        <div className="keywords-list missing">
                            <h4>Missing Keywords</h4>
                            <ul>
                                {analysisResult.missing_important_keywords?.map((kw, i) => <li key={i}>{kw}</li>)}
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ResumeChecker;