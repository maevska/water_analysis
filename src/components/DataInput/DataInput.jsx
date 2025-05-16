import React, { useState } from 'react';
import './DataInput.css';

const DataInput = ({ onSubmit }) => {
    const [waterName, setWaterName] = useState('');
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

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(waterName + ' водоем')}&limit=1`
            );
            
            if (!response.ok) {
                throw new Error('Ошибка при поиске координат');
            }

            const data = await response.json();
            
            if (data && data.length > 0) {
                const coordinates = {
                    lat: parseFloat(data[0].lat),
                    lng: parseFloat(data[0].lon)
                };
                
                onSubmit({
                    waterName,
                    coordinates,
                    parameters
                });
            } else {
                throw new Error('Не удалось найти координаты водоема');
            }
        } catch (error) {
            setError('Не удалось определить координаты водоема. Пожалуйста, проверьте название.');
            console.error('Ошибка:', error);
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
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <label>Название водоема:</label>
                    <input
                        type="text"
                        value={waterName}
                        onChange={(e) => setWaterName(e.target.value)}
                        required
                    />
                </div>

                {error && <div className="error-message">{error}</div>}
                
                <div className="parameters-grid">
                    {Object.entries(parameters).map(([key, value]) => (
                        <div key={key} className="parameter-input">
                            <label>{key}:</label>
                            <input
                                type="number"
                                step="0.1"
                                value={value}
                                onChange={(e) => handleParameterChange(key, e.target.value)}
                                required
                            />
                        </div>
                    ))}
                </div>

                <button 
                    type="submit" 
                    className="submit-button"
                    disabled={loading}
                >
                    {loading ? 'Получение координат...' : 'Получить прогноз'}
                </button>
            </form>
        </div>
    );
};

export default DataInput;