import React from 'react';
import './PredictionDetails.css';

const PredictionDetails = ({ prediction, onClose }) => {
    if (!prediction) return null;

    return (
        <div className="prediction-details-modal">
            <div className="prediction-details-content">
                <button className="close-button" onClick={onClose}>×</button>
                <h3>Детали прогноза</h3>

                <div className="details-section">
                    <h4>Основная информация</h4>
                    <div className="detail-item">
                        <span className="detail-label">Водоем:</span>
                        <span className="detail-value">{prediction.water_name}</span>
                    </div>
                    <div className="detail-item">
                        <span className="detail-label">Дата:</span>
                        <span className="detail-value">{new Date(prediction.created_at).toLocaleString()}</span>
                    </div>
                    <div className="detail-item">
                        <span className="detail-label">Статус:</span>
                        <span className={`detail-value status-${prediction.status}`}>
                            {prediction.status === 'completed' ? 'Успешно' : 'Ошибка'}
                        </span>
                    </div>
                </div>

                {prediction.status === 'completed' && (
                    <>
                        <div className="details-section">
                            <h4>Параметры воды</h4>
                            <div className="parameters-grid-details">
                                {Object.entries(prediction.parameters).map(([key, value]) => (
                                    <div key={key} className="parameter-item">
                                        <span className="parameter-name">{key}</span>
                                        <span className="parameter-value">{typeof value === 'number' ? value.toFixed(2) : value}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="details-section">
                            <h4>Результаты прогноза</h4>
                            <div className="parameters-grid-details">
                                {Object.entries(prediction.results).map(([key, value]) => (
                                    <div key={key} className="parameter-item">
                                        <span className="parameter-name">{key}</span>
                                        <span className="parameter-value">{typeof value === 'number' ? value.toFixed(2) : value}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="details-section">
                            <h4>Класс качества воды</h4>
                            <div className="quality-class-details">
                                {prediction.water_quality_class?.label || 'Н/Д'}
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default PredictionDetails; 