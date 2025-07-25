import React from 'react';
import './PredictionResults.css';

const PredictionResults = ({ predictions, waterQualityClass, plot }) => {
    if (!predictions || !waterQualityClass) {
        return null;
    }

    return (
  <div className="prediction-results">
    <h3>Результаты прогноза</h3>
    <div className="results-wrapper">
      <div className="results-column">
        <div className="results-grid">
          {Object.entries(predictions).map(([parameter, value]) => (
            <div key={parameter} className="result-item">
              <span className="parameter-name">{parameter}</span>
              <span className="parameter-value">
                {typeof value === 'number' ? value.toFixed(2) : value}
              </span>
            </div>
          ))}
        </div>
        <div className="quality-class">
          <h4>Класс качества воды:</h4>
          <p>{waterQualityClass.label}</p>
        </div>
      </div>

      {plot && (
        <div className="plot-container">
          <img 
            src={`data:image/png;base64,${plot}`}
            alt="График сравнения показателей"
            className="plot-image"
          />
        </div>
      )}
    </div>
  </div>
);
};

export default PredictionResults;