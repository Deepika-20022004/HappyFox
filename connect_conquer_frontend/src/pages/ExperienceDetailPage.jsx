import React, { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import AuthContext from '../context/AuthContext';
import './css/ExperiencePage.css';

const ExperienceDetailPage = () => {
    const [experience, setExperience] = useState(null);
    const [newComment, setNewComment] = useState("");
    const { id } = useParams();
    const { user } = useContext(AuthContext);

    useEffect(() => {
        fetchExperience();
    }, [id]);

    const fetchExperience = async () => {
        try {
            const response = await api.get(`/experiences/${id}/`);
            setExperience(response.data);
        } catch (error) {
            console.error("Failed to fetch experience:", error);
        }
    };

    const handleCommentSubmit = async (e) => {
        e.preventDefault();
        if (!newComment.trim()) return;
        try {
            await api.post(`/experiences/${id}/comments/`, { text: newComment });
            setNewComment("");
            fetchExperience(); // Re-fetch to show the new comment
        } catch (error) {
            console.error("Failed to post comment:", error);
        }
    };

    if (!experience) return <div>Loading...</div>;

    return (
        <div className="experience-container detail-view">
            <div className="experience-content">
                <h1>{experience.company_name}</h1>
                <h2>{experience.role}</h2>
                <div className="experience-meta">
                    <span>Shared by: <strong>{experience.author.username}</strong></span>
                    <span className={`verdict ${experience.verdict.toLowerCase()}`}>{experience.verdict}</span>
                </div>
                <p className="experience-full-text">{experience.experience_text}</p>
            </div>

            <div className="comments-section">
                <h3>Comments ({experience.comments_count})</h3>
                {user && (
                    <form onSubmit={handleCommentSubmit} className="comment-form">
                        <textarea
                            value={newComment}
                            onChange={(e) => setNewComment(e.target.value)}
                            placeholder="Add your comment..."
                            rows="3"
                        ></textarea>
                        <button type="submit">Post Comment</button>
                    </form>
                )}
                <div className="comment-list">
                    {experience.comments.map(comment => (
                        <div key={comment.id} className="comment">
                            <p><strong>{comment.author.username}</strong></p>
                            <p>{comment.text}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ExperienceDetailPage;