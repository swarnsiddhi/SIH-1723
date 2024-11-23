import { useState } from 'react';
import axios from 'axios';

const SaveFeaturesForm = () => {
  const [formData, setFormData] = useState({ elongation: '', uts: '', conductivity: '' });
  const [responseData, setResponseData] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(''); // Reset error
    setResponseData(null); // Reset response data
    axios
      .post('/api/save_features', formData)
      .then((response) => setResponseData(response.data))
      .catch((err) => setError(err.response?.data?.error || err.message));
  };

  return (
    <div>
      <h1>Save Features and Get Prediction</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="elongation"
          placeholder="Elongation"
          value={formData.elongation}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="uts"
          placeholder="UTS"
          value={formData.uts}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="conductivity"
          placeholder="Conductivity"
          value={formData.conductivity}
          onChange={handleChange}
          required
        />
        <button type="submit">Save and Predict</button>
      </form>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {responseData && (
        <div>
          <h2>Saved Features</h2>
          <ul>
            <li>Elongation: {responseData.original_values.Elongation[0]}</li>
            <li>UTS: {responseData.original_values.UTS[0]}</li>
            <li>Conductivity: {responseData.original_values.Conductivity[0]}</li>
          </ul>

          <h2>Predictions</h2>
          <pre>{JSON.stringify(responseData.predictions, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default SaveFeaturesForm;
