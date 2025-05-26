import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import InfoWater from './pages/InfoWater/InfoWater';
import WaterQualityAnalysis from './pages/WaterQualityAnalysis/WaterQualityAnalysis';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import './App.css';

const PrivateRoute = ({ children }) => {
    const isAuthenticated = !!localStorage.getItem('token');
    return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            fetch('http://localhost:8000/api/auth/verify', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
                .then(response => {
                    if (!response.ok) {
                        localStorage.removeItem('token');
                        if (window.location.pathname === '/water-quality-analysis') {
                            window.location.href = '/login';
                        }
                    }
                })
                .catch(error => {
                    console.error('Token verification failed:', error);
                    localStorage.removeItem('token');
                    if (window.location.pathname === '/water-quality-analysis') {
                        window.location.href = '/login';
                    }
                });
        }
    }, []);
    return (
        <Router>
            <div className="App">
                <Navbar />
                <main className="main-content">
                    <Routes>
                        <Route path="/" element={<InfoWater />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route
                            path="/water-quality-analysis"
                            element={
                                <PrivateRoute>
                                    <WaterQualityAnalysis />
                                </PrivateRoute>
                            }
                        />
                    </Routes>
                </main>
            </div>
        </Router>
    );
}

export default App;