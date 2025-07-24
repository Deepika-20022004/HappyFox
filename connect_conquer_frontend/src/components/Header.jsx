import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import './css/Header.css'; // We will create this CSS file

const Header = () => {
    const { user, logoutUser } = useContext(AuthContext);
    const navigate = useNavigate();

    const onLogout = () => {
        logoutUser();
        navigate('/login'); // Redirect to login page after logout
    };

    return (
        <div className="header">
            {user ? (
                <>
                    <span>Hello, {user.username}</span>
                    <button onClick={onLogout}>Logout</button>
                </>
            ) : (
                <>
                    <Link to="/login" className="header-link">Login</Link>
                    <Link to="/register" className="header-link register">Register</Link>
                </>
            )}
        </div>
    );
};

export default Header;