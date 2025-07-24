import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import api from '../services/api'; // Use our centralized api service
import './css/AuthPage.css';

const RegisterPage = () => {
    const [error, setError] = useState(null);
    const { loginUser } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;

        try {
            await api.post('/profile/register/', { username, password });
            // After successful registration, log the user in automatically
            await loginUser(username, password);
            // Redirect to the home page or experiences page
            navigate('/experiences');
        } catch (err) {
            setError('Registration failed. Please try a different username.');
            console.error(err);
        }
    };

    return (
        <div className="auth-container">
            <form onSubmit={handleSubmit} className="auth-form">
                <h2>Register</h2>
                {error && <p className="error-message">{error}</p>}
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input type="text" id="username" name="username" required />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" name="password" required />
                </div>
                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export default RegisterPage;