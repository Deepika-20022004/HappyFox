import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import './css/AuthPage.css'; // We will create this CSS file next

const LoginPage = () => {
    const { loginUser } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;
        
        try {
            // 4. Wait for the login to complete
            await loginUser(username, password);
            // 5. Navigate to the main page on success
            navigate('/companies'); 
        } catch (error) {
            // The loginUser function will now throw an error on failure
            // so we can display it to the user.
            alert("Login Failed: Please check your username and password.");
        }
    };

    return (
        <div className="auth-container">
            <form onSubmit={handleSubmit} className="auth-form">
                <h2>Login</h2>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input type="text" id="username" name="username" required />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" name="password" required />
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default LoginPage;