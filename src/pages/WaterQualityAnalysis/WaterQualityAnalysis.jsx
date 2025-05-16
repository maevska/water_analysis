import React, { useState } from 'react';
import DataInput from '../../components/DataInput/DataInput';
import PredictionResults from '../../components/PredictionResults/PredictionResults';
import './WaterQualityAnalysis.css';

const WaterQualityAnalysis = () => {
    const [analysisData, setAnalysisData] = useState({
        waterName: '',
        coordinates: { lat: '', lng: '' },
        parameters: {},
        results: null
    });
    const [error, setError] = useState(null);

    const handleDataSubmit = async (data) => {
        try {
            setError(null);
            const response = await fetch('http://localhost:8000/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Произошла ошибка при получении прогноза');
            }

            const results = await response.json();
            setAnalysisData({ ...data, results });
        } catch (error) {
            console.error('Ошибка при получении прогноза:', error);
            setError(error.message);
        }
    };

    return (
        <div className="water-quality-analysis">
            <h1>Анализ качества воды</h1>
            <DataInput onSubmit={handleDataSubmit} />
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}
            {analysisData.results && (
                <PredictionResults 
                    predictions={analysisData.results.predictions}
                    waterQualityClass={analysisData.results.waterQualityClass}
                />
            )}
        </div>
    );
};

export default WaterQualityAnalysis;