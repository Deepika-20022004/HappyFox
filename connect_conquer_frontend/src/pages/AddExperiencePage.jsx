import React from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './css/AuthPage.css'; // Reuse the auth form styles

const AddExperiencePage = () => {
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const experienceData = {
            company_name: e.target.company_name.value,
            role: e.target.role.value,
            experience_text: e.target.experience_text.value,
            verdict: e.target.verdict.value,
        };

        try {
            await api.post('/experiences/', experienceData);
            navigate('/experiences'); // Redirect after successful post
        } catch (error) {
            console.error("Failed to submit experience:", error);
        }
    };

    return (
        <div className="auth-container">
            <form onSubmit={handleSubmit} className="auth-form" style={{ maxWidth: '600px' }}>
                <h2>Share Your Interview Experience</h2>
                <div className="form-group">
                    <label>Company Name</label>
                    <input type="text" name="company_name" required />
                </div>
                <div className="form-group">
                    <label>Role</label>
                    <input type="text" name="role" required />
                </div>
                <div className="form-group">
                    <label>Verdict</label>
                    <select name="verdict" required>
                        <option value="OFFERED">Offered</option>
                        <option value="REJECTED">Rejected</option>
                        <option value="WAITLISTED">Waitlisted</option>
                        <option value="NO_RESULT">No Result Yet</option>
                    </select>
                </div>
                <div className="form-group">
                    <label>Your Experience</label>
                    <textarea name="experience_text" rows="10" required></textarea>
                </div>
                <button type="submit">Submit Experience</button>
            </form>
        </div>
    );
};

export default AddExperiencePage;