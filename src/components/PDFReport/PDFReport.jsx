import React, { useState } from 'react';
import './PDFReport.css';

const PDFReport = ({ waterData }) => {
    const [isLoading, setIsLoading] = useState(false);

    const generatePDF = async () => {
        try {
            setIsLoading(true);
            
            const reportData = {
                waterName: waterData.waterName,
                coordinates: waterData.coordinates || {},
                predictions: waterData.predictions || {},
                waterQualityClass: waterData.waterQualityClass || {},
                plot: waterData.plot || '',
                parameters: waterData.parameters || {}
            };

            const response = await fetch('http://localhost:8000/api/generate-report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(reportData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Ошибка при создании отчета');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `water-quality-report-${waterData.waterName}.pdf`;
            document.body.appendChild(a);
            a.click();
            
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

        } catch (error) {
            console.error('Ошибка при создании PDF:', error);
            alert('Произошла ошибка при создании отчета');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="report-generator">
            <button 
                onClick={generatePDF} 
                className="generate-report-btn"
                disabled={isLoading}
            >
                {isLoading ? 'Создание отчета...' : 'Скачать отчет'}
            </button>
        </div>
    );
};

export default PDFReport;