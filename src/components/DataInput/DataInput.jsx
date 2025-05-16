import React, { useState } from 'react';
import './DataInput.css';

const DataInput = ({ onSubmit }) => {
    const [waterName, setWaterName] = useState('');
    const [coordinates, setCoordinates] = useState({ lat: '', lng: '' });
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

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ waterName, coordinates, parameters });
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

                <div className="coordinates-group">
                    <label>Координаты:</label>
                    <input
                        type="number"
                        placeholder="Широта"
                        value={coordinates.lat}
                        onChange={(e) => setCoordinates({...coordinates, lat: e.target.value})}
                        required
                    />
                    <input
                        type="number"
                        placeholder="Долгота"
                        value={coordinates.lng}
                        onChange={(e) => setCoordinates({...coordinates, lng: e.target.value})}
                        required
                    />
                </div>
                
                <div className="parameters-grid">
                    {Object.entries(parameters).map(([key, value]) => (
                        <div key={key} className="parameter-input">
                            <label>{key}:</label>
                            <input
                                type="number"
                                step="0.1"
                                value={value}
                                onChange={(e) => setParameters({
                                    ...parameters,
                                    [key]: e.target.value
                                })}
                                required
                            />
                        </div>
                    ))}
                </div>

                <button type="submit" className="submit-button">
                    Получить прогноз
                </button>
            </form>
        </div>
    );
};

export default DataInput;