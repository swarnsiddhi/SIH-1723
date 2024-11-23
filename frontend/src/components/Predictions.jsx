import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Predictions = () => {
  const [predictions, setPredictions] = useState(null);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await axios.get('/api/predict');
        setPredictions(response.data);
      } catch (error) {
        console.error('Error fetching predictions:', error);
      }
    };

    fetchPredictions();
  }, []);

  return (
    <div>
      <h2>Predictions</h2>
      {predictions ? (
        <pre>{JSON.stringify(predictions, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Predictions;
