import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Predictions = () => {
  const [redirectUrl, setRedirectUrl] = useState(null);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await axios.get('http://localhost:5000/predict');
        setRedirectUrl(response.data.url);
      } catch (error) {
        console.error('Error running prediction:', error);
        alert('Error running prediction.');
      }
    };
    fetchPredictions();
  }, []);

  if (redirectUrl) {
    window.location.href = redirectUrl;
  }

  return <h2>Loading Predictions...</h2>;
};

export default Predictions;
