import { useEffect, useState } from 'react';
import axios from 'axios';

const PredictPage = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    axios.get('/api/predict')
      .then(response => setData(response.data))
      .catch(err => setError(err.message));
  }, []);

  return (
    <div>
      <h1>Prediction Results</h1>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {data ? (
        <ul>
          <li>Elongation: {data.elongation}</li>
          <li>UTS: {data.uts}</li>
          <li>Conductivity: {data.conductivity}</li>
        </ul>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default PredictPage;
