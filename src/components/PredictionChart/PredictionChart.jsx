// filepath: d:\C=D\models_for_VKR\my-website-project\frontend\src\components\PredictionChart\PredictionChart.jsx
import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import './PredictionChart.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

// ...остальной код компонента...

const PredictionChart = ({ inputValues, predictions }) => {
const data = {
    labels: ['Мутность', 'Кислород', 'Уровень воды'],
    datasets: [
    {
        label: 'Текущие показатели',
        data: inputValues,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
    },
    {
        label: 'Прогноз',
        data: predictions,
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
    }
    ]
};

return (
    <div className="chart-container">
    <h3>График сравнения показателей</h3>
    <Bar data={data} options={{
        responsive: true,
        scales: {
        y: {
        beginAtZero: true
        }
        }
    }} />
    </div>
);
};

export default PredictionChart;