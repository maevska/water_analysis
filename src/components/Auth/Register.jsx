import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css';

const Register = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        confirmPassword: '',
        firstName: '',
        lastName: ''
    });
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (formData.password !== formData.confirmPassword) {
            setError('Пароли не совпадают');
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Ошибка при регистрации');
            }

            navigate('/login');
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-form">
                <h2>Регистрация</h2>
                {error && <div className="auth-error">{error}</div>}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Имя пользователя:</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            pattern="[a-zA-Z0-9_]+"
                            title="Имя пользователя должно содержать только буквы, цифры и символ подчеркивания"
                            minLength="3"
                            maxLength="50"
                        />
                    </div>
                    <div className="form-group">
                        <label>Имя:</label>
                        <input
                            type="text"
                            name="firstName"
                            value={formData.firstName}
                            onChange={handleChange}
                            required
                            pattern="[а-яА-Яa-zA-Z\s-]+"
                            title="Имя должно содержать только буквы, пробелы и дефисы"
                            minLength="2"
                            maxLength="50"
                        />
                    </div>
                    <div className="form-group">
                        <label>Фамилия:</label>
                        <input
                            type="text"
                            name="lastName"
                            value={formData.lastName}
                            onChange={handleChange}
                            required
                            pattern="[а-яА-Яa-zA-Z\s-]+"
                            title="Фамилия должна содержать только буквы, пробелы и дефисы"
                            minLength="2"
                            maxLength="50"
                        />
                    </div>
                    <div className="form-group">
                        <label>Email:</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Пароль:</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            minLength="6"
                            pattern="(?=.*[A-Z])(?=.*[a-z])(?=.*\d).*"
                            title="Пароль должен содержать минимум 6 символов, хотя бы одну заглавную букву, одну строчную букву и одну цифру"
                        />
                    </div>
                    <div className="form-group">
                        <label>Подтвердите пароль:</label>
                        <input
                            type="password"
                            name="confirmPassword"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <button type="submit" className="auth-button">Зарегистрироваться</button>
                </form>
                <p className="auth-switch">
                    Уже есть аккаунт? <span onClick={() => navigate('/login')}>Войти</span>
                </p>
            </div>
        </div>
    );
};

export default Register;