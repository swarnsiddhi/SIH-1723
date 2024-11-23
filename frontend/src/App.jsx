import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import PredictPage from './pages/PredictPage';
import FinalPredictionPage from './pages/FinalPredictionPage';

const App = () => (
  <>
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/predict">Prediction</Link></li>
        <li><Link to="/save-features">Save Features</Link></li>
        <li><Link to="/final-prediction">Final Prediction</Link></li>
      </ul>
    </nav>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/predict" element={<PredictPage />} />
      <Route path="/save-features" element={<SaveFeaturesForm />} />
      <Route path="/final-prediction" element={<FinalPredictionPage />} />
    </Routes>
  </>
);

export default App;
