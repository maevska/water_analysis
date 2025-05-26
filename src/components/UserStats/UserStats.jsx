import React from 'react';
import './UserStats.css';

const UserStats = ({ stats }) => {
  if (!stats) return null;

  return (
    <div className="user-stats">
      <h3>Статистика прогнозов</h3>
      <div className="stats-grid">
        <div className="stat-item">
          <span className="stat-label">Всего прогнозов</span>
          <span className="stat-value">{stats.total_predictions || 0}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Успешных</span>
          <span className="stat-value success">{stats.completed_predictions || 0}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">С ошибками</span>
          <span className="stat-value error">{stats.error_predictions || 0}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Последний прогноз</span>
          <span className="stat-value">
            {stats.last_prediction_date ? new Date(stats.last_prediction_date).toLocaleString() : 'Нет данных'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default UserStats;