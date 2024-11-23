import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Results = () => {
  const [results, setResults] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await axios.get('/api/final_prediction');
        setResults(response.data);
      } catch (error) {
        console.error('Error fetching results:', error);
      }
    };

    fetchResults();
  }, []);

  return (
    <div>
      <h2>Results</h2>
      {results ? (
        <pre>{JSON.stringify(results, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Results;
