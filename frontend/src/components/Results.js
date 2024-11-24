import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Results = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await axios.get('http://localhost:5000/final_prediction');
        setData(response.data);
      } catch (error) {
        console.error('Error fetching results:', error);
        alert('Error fetching results.');
      }
    };
    fetchResults();
  }, []);

  return (
    <div>
      <h2>Results</h2>
      {data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Results;
