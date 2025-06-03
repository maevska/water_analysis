import React, { useState, useEffect, useRef } from 'react';
import './UserProfile.css';
import UserStats from '../UserStats/UserStats';
import PredictionHistory from '../PredictionHistory/PredictionHistory';
import { waterApi } from '../../api/water.api';

const UserProfile = ({ isOpen, onClose }) => {
    const [userData, setUserData] = useState(null);
    const [userStats, setUserStats] = useState(null);
    const [predictions, setPredictions] = useState([]);
    const [error, setError] = useState(null);
    const [uploading, setUploading] = useState(false);
    const fileInputRef = useRef(null);

    const fetchUserData = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                setError('Требуется авторизация');
                return;
            }

            const response = await fetch('http://localhost:8000/api/users/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                if (response.status === 401) {
                    localStorage.removeItem('token');
                    window.location.href = '/login';
                    return;
                }
                throw new Error('Ошибка при получении данных пользователя');
            }

            const data = await response.json();
            setUserData(data);

            const stats = await waterApi.getUserStats(data.id);
            setUserStats(stats);

            const predictionHistory = await waterApi.getUserPredictions(data.id);
            setPredictions(predictionHistory);

            setError(null);
        } catch (error) {
            console.error('Error fetching user data:', error);
            setError(error.message);
        }
    };

    useEffect(() => {
        if (isOpen) {
            fetchUserData();
        }
    }, [isOpen]);

    useEffect(() => {
        const handleProfileUpdate = (event) => {
            const { stats, predictions } = event.detail;
            setUserStats(stats);
            setPredictions(predictions);
        };

        window.addEventListener('profileDataUpdated', handleProfileUpdate);

        return () => {
            window.removeEventListener('profileDataUpdated', handleProfileUpdate);
        };
    }, []);

    const handlePhotoUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
            setError('Пожалуйста, выберите изображение');
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            setError('Размер файла не должен превышать 5MB');
            return;
        }

        setUploading(true);
        setError(null);

        try {
            const token = localStorage.getItem('token');
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('http://localhost:8000/api/users/me/photo', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Ошибка при загрузке фото');
            }

            const data = await response.json();
            setUserData(prev => ({
                ...prev,
                profile_photo: data.photo_path
            }));
        } catch (error) {
            console.error('Error uploading photo:', error);
            setError(error.message);
        } finally {
            setUploading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className={`user-profile-modal ${isOpen ? 'open' : ''}`}>
            <div className="user-profile-content">
                <button className="close-button" onClick={onClose}>×</button>
                <div className="user-profile-header">
                    <h2>Личный кабинет</h2>
                </div>
                <div className="user-profile-body">
                    {error ? (
                        <div className="error-message">{error}</div>
                    ) : userData ? (
                        <>
                            <div className="profile-photo-container">
                                {userData.profile_photo ? (
                                    <img
                                        src={`http://localhost:8000/${userData.profile_photo}`}
                                        alt="Фото профиля"
                                        className="profile-photo"
                                        onError={(e) => {
                                            e.target.style.display = 'none';
                                            e.target.parentElement.querySelector('.profile-photo-placeholder').style.display = 'flex';
                                        }}
                                    />
                                ) : null}
                                {!userData.profile_photo && (
                                    <div className="profile-photo-placeholder">
                                        {userData.firstName?.[0]}{userData.lastName?.[0]}
                                    </div>
                                )}
                                <div className="photo-upload-container">
                                    <input
                                        type="file"
                                        accept="image/*"
                                        onChange={handlePhotoUpload}
                                        ref={fileInputRef}
                                        style={{ display: 'none' }}
                                    />
                                    <button
                                        className="upload-photo-button"
                                        onClick={() => fileInputRef.current?.click()}
                                        disabled={uploading}
                                    >
                                        {uploading ? 'Загрузка...' : 'Изменить фото'}
                                    </button>
                                </div>
                            </div>
                            <div className="profile-field">
                                <label>Имя пользователя:</label>
                                <span>{userData.username}</span>
                            </div>
                            <div className="profile-field">
                                <label>Email:</label>
                                <span>{userData.email}</span>
                            </div>
                            <div className="profile-field">
                                <label>Имя:</label>
                                <span>{userData.firstName}</span>
                            </div>
                            <div className="profile-field">
                                <label>Фамилия:</label>
                                <span>{userData.lastName}</span>
                            </div>
                            {userStats && <UserStats stats={userStats} />}
                            {predictions.length > 0 && <PredictionHistory predictions={predictions} />}
                        </>
                    ) : (
                        <div className="loading">Загрузка данных...</div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default UserProfile;