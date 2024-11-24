import React from 'react';

const FeatureInput = ({ features, handleInputChange }) => {
    return (
        <div style={{ marginBottom: '15px' }}>
            <input
                type="number"
                name="elongation"
                placeholder="Elongation"
                value={features.elongation}
                onChange={handleInputChange}
                style={{ marginRight: '10px', padding: '5px', width: '150px' }}
            />
            <input
                type="number"
                name="uts"
                placeholder="UTS"
                value={features.uts}
                onChange={handleInputChange}
                style={{ marginRight: '10px', padding: '5px', width: '150px' }}
            />
            <input
                type="number"
                name="conductivity"
                placeholder="Conductivity"
                value={features.conductivity}
                onChange={handleInputChange}
                style={{ padding: '5px', width: '150px' }}
            />
        </div>
    );
};

export default FeatureInput;
