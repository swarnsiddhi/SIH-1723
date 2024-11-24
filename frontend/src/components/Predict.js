import React, { useState } from 'react';

function Predict() {
  const [message, setMessage] = useState('');

  const runPrediction = async () => {
    try {
      const response = await fetch('/predict', { method: 'GET' });
      const result = await response.json();

      if (response.ok) {
        setMessage('Prediction successful. Redirecting...');
        window.location.href = `/final-prediction?elongation=${result.elongation}&uts=${result.uts}&conductivity=${result.conductivity}`;
      } else {
        setMessage(`Error: ${result.error}`);
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  return (
    <div>
      <h2>Predict</h2>
      <button onClick={runPrediction}>Run Prediction</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default Predict;
