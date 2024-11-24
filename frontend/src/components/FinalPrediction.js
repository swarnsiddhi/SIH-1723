import React, { useEffect, useState } from 'react';

function FinalPrediction() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/final_prediction');
        const result = await response.json();

        if (response.ok) {
          setData(result);
        } else {
          setError(result.error);
        }
      } catch (error) {
        setError(`Error: ${error.message}`);
      }
    };

    fetchData();
  }, []);

  if (error) {
    return <p>{error}</p>;
  }

  if (!data) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h2>Final Prediction</h2>
      <h3>Original Values:</h3>
      <pre>{JSON.stringify(data.original_values, null, 2)}</pre>
      <h3>Predicted Values:</h3>
      <pre>{JSON.stringify(data.predictions, null, 2)}</pre>
      <h3>Differences:</h3>
      <pre>{JSON.stringify(data.differences, null, 2)}</pre>
    </div>
  );
}

export default FinalPrediction;
