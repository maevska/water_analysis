import React, { useState } from 'react';
import './DataInput.css';
import { waterApi } from '../../api/water.api';

const DataInput = ({ onSubmit, disabled, onUnlock, showUnlockButton, initialData }) => {
    const [waterName, setWaterName] = useState(initialData?.waterName || '');
    const [parameters, setParameters] = useState({
        temp_water: '',
        temp_air: '',
        precipitation: '',
        water_level: '',
        ph: '',
        turbidity: '',
        oxygen: '',
        nitrates: '',
        ammonia: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [csvFile, setCsvFile] = useState(null);

    const handleReset = () => {
        setWaterName('');
        setParameters({
            temp_water: '',
            temp_air: '',
            precipitation: '',
            water_level: '',
            ph: '',
            turbidity: '',
            oxygen: '',
            nitrates: '',
            ammonia: ''
        });
        setCsvFile(null);
        onUnlock();
    };

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (file && file.type === 'text/csv') {
            setCsvFile(file);
            setLoading(true);
            setError(null);

            try {
                const response = await waterApi.uploadCSV(file);
                setWaterName(response.waterName);
                setParameters(response.parameters);
                setError(null);
            } catch (error) {
                setError(error.message);
                setCsvFile(null);
            } finally {
                setLoading(false);
            }
        } else {
            setError('Пожалуйста, загрузите файл в формате CSV');
            setCsvFile(null);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(waterName + ' водоем')}&limit=1`
            );

            if (!response.ok) {
                throw new Error('Не удалось определить координаты водоема, проверьте название водоема');
            }

            const data = await response.json();

            if (!data || data.length === 0) {
                throw new Error('Не удалось определить координаты водоема, проверьте название водоема');
            }

            const coordinates = {
                lat: parseFloat(data[0].lat),
                lng: parseFloat(data[0].lon)
            };

            const validatedParameters = {};
            for (const [key, value] of Object.entries(parameters)) {
                const numValue = parseFloat(value);
                if (isNaN(numValue)) {
                    throw new Error(`Поле "${key}" должно быть числом`);
                }
                validatedParameters[key] = numValue;
            }

            onSubmit({
                waterName,
                coordinates,
                parameters: validatedParameters
            });
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleParameterChange = (key, value) => {
        setParameters(prev => ({
            ...prev,
            [key]: value
        }));
    };

    return (
        <div className="data-input-container">
            <h2>Ввод гидробиологических данных</h2>
            <form onSubmit={handleSubmit} className="data-input-form">
                <div className="input-group">
                    <label>Название водоема:</label>
                    <input
                        className="NameLabel"
                        type="text"
                        value={waterName}
                        onChange={(e) => setWaterName(e.target.value)}
                        required
                        disabled={disabled}
                    />
                </div>

                <div className="csv-upload-container">
                    <label className="csv-upload-label">
                        {loading ? 'Загрузка...' : 'Загрузить данные из CSV'}
                        <input
                            type="file"
                            accept=".csv"
                            onChange={handleFileUpload}
                            disabled={disabled || loading}
                            className="csv-upload-input"
                        />
                    </label>
                    {csvFile && (
                        <span className="csv-file-name">
                            Выбран файл: {csvFile.name}
                        </span>
                    )}
                </div>

                {error && <div className="error-message">{error}</div>}

                <div className="parameters-grid">
                    {Object.entries(parameters).map(([key, value]) => (
                        <div key={key} className="parameter-input">
                            <label>{key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}:</label>
                            <input
                                type="number"
                                step="0.1"
                                value={value}
                                onChange={(e) => handleParameterChange(key, e.target.value)}
                                required
                                disabled={disabled}
                            />
                        </div>
                    ))}
                </div>
                <div className="button-container">
                    <button
                        type="submit"
                        className="submit-button"
                        disabled={disabled || loading}
                    >
                        {loading ? 'Получение координат...' : 'Получить прогноз'}
                    </button>
                    {showUnlockButton && (
                        <button
                            type="button"
                            className="submit-button unlock-button"
                            onClick={handleReset}
                        >
                            Новый прогноз
                        </button>
                    )}
                </div>
            </form>
        </div>
    );
};

export default DataInput;