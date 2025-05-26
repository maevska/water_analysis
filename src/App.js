import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import InfoWater from './pages/InfoWater/InfoWater';
import WaterQualityAnalysis from './pages/WaterQualityAnalysis/WaterQualityAnalysis';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<InfoWater />} />
          <Route path="/water-quality-analysis" element={<WaterQualityAnalysis />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;