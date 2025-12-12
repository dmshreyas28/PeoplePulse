import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictEmployee = async (employeeData) => {
  const response = await api.post('/api/predict/employee', employeeData);
  return response.data;
};

export const predictBatch = async (employees) => {
  const response = await api.post('/api/predict/batch', { employees });
  return response.data;
};

export const simulateIntervention = async (employeeId, currentData, proposedChanges) => {
  const response = await api.post('/api/simulate/intervention', {
    employee_id: employeeId,
    current_data: currentData,
    proposed_changes: proposedChanges,
  });
  return response.data;
};

export const getEmployees = async (skip = 0, limit = 100) => {
  const response = await api.get(`/api/employees?skip=${skip}&limit=${limit}`);
  return response.data;
};

export const getEmployee = async (employeeId) => {
  const response = await api.get(`/api/employees/${employeeId}`);
  return response.data;
};

export const createEmployee = async (employeeData) => {
  const response = await api.post('/api/employees', employeeData);
  return response.data;
};

export const getPredictionHistory = async (employeeId) => {
  const response = await api.get(`/api/predict/history/${employeeId}`);
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
