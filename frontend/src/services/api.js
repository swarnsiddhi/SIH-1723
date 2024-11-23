import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

export const fetchPredictions = () => api.get('/predict');
export const saveFeatures = (data) => api.post('/save_features', data);
export const fetchFinalPrediction = (params) =>
  api.get('/final_prediction', { params });

export default api;
