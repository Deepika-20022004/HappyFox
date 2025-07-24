import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode'; // We need to install this library
import axios from 'axios';

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
    // Get tokens from localStorage, or set to null if they don't exist
    const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
    // Decode the user from the access token
    const [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null);

    const loginUser = async (username, password) => {
        try {
            const response = await axios.post('http://localhost:8000/api/token/', {
                username,
                password
            });
            
            if (response.status === 200) {
                setAuthTokens(response.data);
                setUser(jwtDecode(response.data.access));
                localStorage.setItem('authTokens', JSON.stringify(response.data));
                // No need to navigate here, the component will do it.
            }
        } catch (error) {
            // If the login fails (e.g. 401 Unauthorized), an error will be caught.
            console.error("Login error:", error);
            // Re-throw the error so the component can catch it and display an alert.
            throw error;
        }
    };

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
    };

    const contextData = {
        user: user,
        authTokens: authTokens,
        loginUser: loginUser,
        logoutUser: logoutUser,
    };

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    );
};