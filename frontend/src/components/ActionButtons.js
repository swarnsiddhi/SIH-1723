import React from 'react';

const ActionButtons = ({ handleSave, handlePredict }) => {
    return (
        <div>
            <button onClick={handleSave} style={{ marginRight: '10px', padding: '10px 15px' }}>Save Features</button>
            <button onClick={handlePredict} style={{ padding: '10px 15px' }}>Get Predictions</button>
        </div>
    );
};

export default ActionButtons;
