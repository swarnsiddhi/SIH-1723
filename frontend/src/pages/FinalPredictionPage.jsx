import { useState } from 'react';
import axios from 'axios';

const FinalPredictionPage = () => {
  const [formData, setFormData] = useState({ elongation: '', uts: '', conductivity: '' });
  const [predictions, setPredictions] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/api/final_prediction', formData)
      .then(response => setPredictions(response.data))
      .catch(err => setError(err.message));
  };

  return (
    <div>
      <h1>Final Prediction</h1>
      <form onSubmit={handleSubmit}>
        <input name="elongation" placeholder="Elongation" value={formData.elongation} onChange={handleChange} />
        <input name="uts" placeholder="UTS" value={formData.uts} onChange={handleChange} />
        <input name="conductivity" placeholder="Conductivity" value={formData.conductivity} onChange={handleChange} />
        <button type="submit">Get Prediction</button>
      </form>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {predictions && (
        <div>
          <h2>Predictions</h2>
          <p>{JSON.stringify(predictions)}</p>
        </div>
      )}
    </div>
  );
};

export default FinalPredictionPage;
