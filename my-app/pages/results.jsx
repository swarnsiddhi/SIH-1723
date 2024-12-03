import React, { useEffect, useState } from "react";
import '@/app/globals.css';
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
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 text-white p-8">
      <h1 className="text-3xl font-bold mb-8">Prediction Results</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-6xl">
        {/* Left Column: Elongation, UTS, Conductivity */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow-md text-gray-900">
            <h2 className="text-lg font-semibold mb-2">Elongation</h2>
            <p>{results.elongation}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md text-gray-900">
            <h2 className="text-lg font-semibold mb-2">UTS</h2>
            <p>{results.uts}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md text-gray-900">
            <h2 className="text-lg font-semibold mb-2">Conductivity</h2>
            <p>{results.conductivity}</p>
          </div>
        </div>

        {/* Right Column: Differences */}
        <div className="grid grid-cols-1 gap-4">
          {Object.entries(results.differences || {}).map(([key, value]) => (
            <div
              key={key}
              className="bg-white p-6 rounded-lg shadow-md text-gray-900"
            >
              <h3 className="text-lg font-semibold mb-2">
                {key.replace("_", " ")}
              </h3>
              <p>{value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Result;
