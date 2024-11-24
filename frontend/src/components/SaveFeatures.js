import React, { useState } from 'react';

function SaveFeatures() {
  const [formData, setFormData] = useState({ elongation: '', uts: '', conductivity: '' });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/save_features', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(formData),
      });

      const result = await response.json();
      setMessage(result.message || `Error: ${result.error}`);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  return (
    <div>
      <h2>Save Features</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          name="elongation"
          placeholder="Elongation"
          value={formData.elongation}
          onChange={handleChange}
        />
        <input
          type="number"
          name="uts"
          placeholder="UTS"
          value={formData.uts}
          onChange={handleChange}
        />
        <input
          type="number"
          name="conductivity"
          placeholder="Conductivity"
          value={formData.conductivity}
          onChange={handleChange}
        />
        <button type="submit">Save</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default SaveFeatures;
