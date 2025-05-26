import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import UserProfile from '../UserProfile/UserProfile';
import './Navbar.css';

const Navbar = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const isAuthenticated = !!localStorage.getItem('token');
    const [isProfileOpen, setIsProfileOpen] = useState(false);

    if (location.pathname !== '/water-quality-analysis') {
        return null;
    }

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    const toggleProfile = () => {
        setIsProfileOpen(!isProfileOpen);
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <div className="navbar-logo" onClick={() => navigate('/')}>
                    WaterQS
                </div>
                <div className="nav-auth">
                    {isAuthenticated && (
                        <>
                            <button onClick={toggleProfile} className="nav-button profile-button">
                                Профиль
                            </button>
                            <button onClick={handleLogout} className="nav-button">
                                Выйти
                            </button>
                        </>
                    )}
                </div>
            </div>
            <UserProfile isOpen={isProfileOpen} onClose={() => setIsProfileOpen(false)} />
        </nav>
    );
};

export default Navbar;