import React, { useState } from 'react';
import axios from 'axios';

const ManualInput = () => {
  const [features, setFeatures] = useState({
    elongation: '',
    uts: '',
    conductivity: ''
  });

  const handleChange = (e) => {
    setFeatures({ ...features, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/save_features', features);
      alert(response.data.message);
    } catch (error) {
      console.error('Error saving features:', error);
      alert('Error saving features.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Manual Input</h2>
      <input
        type="text"
        name="elongation"
        placeholder="Elongation"
        value={features.elongation}
        onChange={handleChange}
      />
      <input
        type="text"
        name="uts"
        placeholder="UTS"
        value={features.uts}
        onChange={handleChange}
      />
      <input
        type="text"
        name="conductivity"
        placeholder="Conductivity"
        value={features.conductivity}
        onChange={handleChange}
      />
      <button type="submit">Save Features</button>
    </form>
  );
};

export default ManualInput;
