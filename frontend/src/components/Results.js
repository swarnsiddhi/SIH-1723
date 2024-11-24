import React from 'react';

const Results = ({ results }) => {
    return (
        <div style={{ marginTop: '20px' }}>
            <h2>Results</h2>
            <div>
                <h3>Predicted Values</h3>
                <p><strong>Elongation:</strong> {results.predictions.elongation}</p>
                <p><strong>UTS:</strong> {results.predictions.uts}</p>
                <p><strong>Conductivity:</strong> {results.predictions.conductivity}</p>
            </div>
            <div>
                <h3>Differences</h3>
                <p><strong>Predicted aluminium_purity:</strong> {results.differences.A}</p>
                <p><strong>Predicted casting_temperature:</strong> {results.differences.B}</p>
                <p><strong>Predicted cooling_water_temp:</strong> {results.differences.C}</p>
                <p><strong>Predicted casting_speed:</strong> {results.differences.D}</p>
                <p><strong>Predicted rolling_mill_temp:</strong> {results.differences.E}</p>
                <p><strong>Predicted emulsion_temp:</strong> {results.differences.F}</p>
                <p><strong>Predicted emulsion_pressure:</strong> {results.differences.G}</p>
                <p><strong>Predicted emulsion_conc:</strong> {results.differences.H}</p>
                <p><strong>Predicted rod_quench_temp:</strong> {results.differences.I}</p>
            </div>
        </div>
    );
};

export default Results;
