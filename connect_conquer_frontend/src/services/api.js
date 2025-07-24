import axios from 'axios';

const baseURL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL,
});

// This is an interceptor. It runs before every request.
api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')).access : null;
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

export default api;