import React, { useState } from 'react';
import DataInput from '../../components/DataInput/DataInput';
import PredictionResults from '../../components/PredictionResults/PredictionResults';
import Map from '../../components/Map/Map';
import PDFReport from '../../components/PDFReport/PDFReport';
import './WaterQualityAnalysis.css';

const WaterQualityAnalysis = () => {
    const [analysisData, setAnalysisData] = useState({
        waterName: '',
        coordinates: { lat: '', lng: '' },
        parameters: {},
        results: null
    });
    const [error, setError] = useState(null);
    const [isLocked, setIsLocked] = useState(false);

    const handleDataSubmit = async (data) => {
        try {
            setError(null);
            setAnalysisData(prevData => ({
                ...prevData,
                waterName: data.waterName,
                coordinates: data.coordinates,
                parameters: data.parameters
            }));

            const response = await fetch('http://localhost:8000/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Произошла ошибка при получении прогноза');
            }

            const results = await response.json();
            setAnalysisData(prevData => ({ ...prevData, results }));
            setIsLocked(true);

            const userData = await fetch('http://localhost:8000/api/users/me', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            }).then(res => res.json());

            const statsResponse = await fetch(`http://localhost:8000/api/users/${userData.id}/stats`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const stats = await statsResponse.json();

            const predictionsResponse = await fetch(`http://localhost:8000/api/users/${userData.id}/predictions`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const predictions = await predictionsResponse.json();

            window.dispatchEvent(new CustomEvent('profileDataUpdated', {
                detail: { stats, predictions }
            }));

        } catch (error) {
            setError(error.message);
        }
    };

    const handleUnlock = () => {
        setIsLocked(false);
    };

    return (
        <div className={`analysis-page ${analysisData.results ? 'has-results' : ''}`}>
            <h1>Анализ качества воды</h1>
            <div className={`analysis-content ${analysisData.results ? 'with-map' : 'centered'}`}>
                <div className="data-input-container">
                    <DataInput
                        onSubmit={handleDataSubmit}
                        initialData={analysisData}
                        disabled={isLocked}
                        onUnlock={handleUnlock}
                        showUnlockButton={isLocked}
                    />
                </div>
                {analysisData.results && (
                    <div className="map-container">
                        <Map
                            waterName={analysisData.waterName}
                            coordinates={analysisData.coordinates}
                        />
                    </div>
                )}
            </div>
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}
            {analysisData.results && (
                <div className="prediction-results">
                    <PredictionResults
                        predictions={analysisData.results.predictions}
                        waterQualityClass={analysisData.results.waterQualityClass}
                        plot={analysisData.results.plot}
                    />
                    <PDFReport
                        waterData={{
                            waterName: analysisData.waterName,
                            coordinates: analysisData.coordinates,
                            parameters: analysisData.parameters,
                            ...analysisData.results
                        }}
                    />
                </div>
            )}
        </div>
    );
};

export default WaterQualityAnalysis;