import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const saveFeatures = (features) => {
    return axios.post(`${API_BASE_URL}/save_features`, features);
};

export const getFinalPrediction = (params) => {
    return axios.get(`${API_BASE_URL}/final_prediction`, { params });
};