import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ManualInput from './components/ManualInput';
import Predictions from './components/Predictions';
import Results from './components/Results';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/predictions">Predictions</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<ManualInput />} />
          <Route path="/predictions" element={<Predictions />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
