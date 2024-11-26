import React, { useEffect, useState } from "react";

const Result = () => {
  const [results, setResults] = useState(null);

  useEffect(() => {
    const storedResults = localStorage.getItem("predictionResults");
    if (storedResults) {
      setResults(JSON.parse(storedResults));
    }
  }, []);

  if (!results) {
    return (
      <p className="min-h-screen flex items-center justify-center text-white">
        No results to display. Please try predicting again.
      </p>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 text-white p-4">
      <h1 className="text-2xl font-bold mb-4">Prediction Results</h1>
      <div className="bg-white p-6 rounded-lg shadow-md text-gray-900">
        <h2 className="text-lg font-semibold mb-2">Predicted Values</h2>
        <p>
          <strong>Elongation:</strong> {results.elongation}
        </p>
        <p>
          <strong>UTS:</strong> {results.uts}
        </p>
        <p>
          <strong>Conductivity:</strong> {results.conductivity}
        </p>

        <h2 className="text-lg font-semibold mt-4 mb-2">Differences</h2>
        {Object.entries(results.differences || {}).map(([key, value]) => (
          <p key={key}>
            <strong>{key.replace("_", " ")}:</strong> {value}
          </p>
        ))}
      </div>
    </div>
  );
};

export default Result;
