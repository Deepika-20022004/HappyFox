import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import AuthContext from '../context/AuthContext';
import './css/ExperiencePage.css';

const ExperienceListPage = () => {
    const [experiences, setExperiences] = useState([]);
    const { user } = useContext(AuthContext);

    useEffect(() => {
        const fetchExperiences = async () => {
            try {
                const response = await api.get('/experiences/');
                setExperiences(response.data);
            } catch (error) {
                console.error("Failed to fetch experiences:", error);
            }
        };
        fetchExperiences();
    }, []);

    return (
        <div className="experience-container">
            <div className="experience-header">
                <h1>Interview Experiences</h1>
                {user && (
                    <Link to="/add-experience" className="add-experience-btn">
                        + Share Your Experience
                    </Link>
                )}
            </div>
            <div className="experience-list">
                {experiences.map(exp => (
                    <div key={exp.id} className="experience-card">
                        <h3><Link to={`/experiences/${exp.id}`}>{exp.company_name} - {exp.role}</Link></h3>
                        <p className="author">Shared by: {exp.author.username}</p>
                        <p className="experience-snippet">{exp.experience_text.substring(0, 150)}...</p>
                        <div className="card-footer">
                            <span className={`verdict ${exp.verdict.toLowerCase()}`}>{exp.verdict}</span>
                            <span>{exp.comments_count} comments</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ExperienceListPage;