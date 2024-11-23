import React, { useState } from 'react';


const FeatureForm = () => {
    const [formData, setFormData] = useState({ elongation: '', uts: '', conductivity: '' });
    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/save_features', formData);
            setMessage('Features saved successfully!');
            setFormData({ elongation: '', uts: '', conductivity: '' });
        } catch (error) {
            setMessage('Error saving features: ' + error.message);
        }
    };

    return (
        <div className="container">
            <h2>Save Features</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="elongation" className="form-label">Elongation</label>
                    <input
                        type="number"
                        className="form-control"
                        id="elongation"
                        name="elongation"
                        value={formData.elongation}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="uts" className="form-label">UTS</label>
                    <input
                        type="number"
                        className="form-control"
                        id="uts"
                        name="uts"
                        value={formData.uts}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="conductivity" className="form-label">Conductivity</label>
                    <input
                        type="number"
                        className="form-control"
                        id="conductivity"
                        name="conductivity"
                        value={formData.conductivity}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">Save Features</button>
            </form>
            {message && <div className="alert alert-info mt-3">{message}</div>}
        </div>
    );
};

export default FeatureForm;
