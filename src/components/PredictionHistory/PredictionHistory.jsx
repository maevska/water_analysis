import React, { useState } from 'react';
import PredictionDetails from '../PredictionDetails/PredictionDetails';
import './PredictionHistory.css';

const PredictionHistory = ({ predictions }) => {
  const [selectedPrediction, setSelectedPrediction] = useState(null);

  if (!predictions || predictions.length === 0) {
    return (
      <div className="prediction-history">
        <h3>История прогнозов</h3>
        <p className="no-predictions">Нет данных о прогнозах</p>
      </div>
    );
  }

  return (
    <div className="prediction-history">
      <h3>История прогнозов</h3>
      <div className="history-table">
        <table>
          <thead>
            <tr>
              <th>Дата</th>
              <th>Водоем</th>
              <th>Класс качества</th>
              <th>Статус</th>
              <th>Детали</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map(prediction => (
              <tr key={prediction.id}>
                <td>{new Date(prediction.created_at).toLocaleString()}</td>
                <td>{prediction.water_name}</td>
                <td>
                  {prediction.water_quality_class?.label || 'Н/Д'}
                </td>
                <td>
                  <span className={`status-${prediction.status}`}>
                    {prediction.status === 'completed' ? 'Успешно' : 'Ошибка'}
                  </span>
                </td>
                <td>
                  <button
                    className="details-button"
                    onClick={() => setSelectedPrediction(prediction)}
                  >
                    Просмотр
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedPrediction && (
        <PredictionDetails
          prediction={selectedPrediction}
          onClose={() => setSelectedPrediction(null)}
        />
      )}
    </div>
  );
};

export default PredictionHistory;