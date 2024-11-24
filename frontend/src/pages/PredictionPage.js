import React, { useState } from 'react';
import { saveFeatures, getFinalPrediction } from '../api';
import FeatureInput from '../components/FeatureInput';
import Results from '../components/Results';
import ActionButtons from '../components/ActionButtons';

const PredictionPage = () => {
    const [features, setFeatures] = useState({ elongation: '', uts: '', conductivity: '' });
    const [results, setResults] = useState(null);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFeatures({ ...features, [name]: value });
    };

    const handleSave = async () => {
        try {
            await saveFeatures(features);
            alert('Features saved successfully!');
        } catch (err) {
            console.error('Error saving features:', err);
            alert('Failed to save features.');
        }
    };

    const handlePredict = async () => {
        try {
            const response = await getFinalPrediction(features);
            setResults(response.data);
        } catch (err) {
            console.error('Error fetching predictions:', err);
            alert('Failed to fetch predictions.');
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto', fontFamily: 'Arial, sans-serif' }}>
            <h1>Feature Prediction</h1>
            <FeatureInput features={features} handleInputChange={handleInputChange} />
            <ActionButtons handleSave={handleSave} handlePredict={handlePredict} />
            {results && <Results results={results} />}
        </div>
    );
};

export default PredictionPage;
