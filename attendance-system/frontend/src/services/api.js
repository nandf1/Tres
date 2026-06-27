import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Employee API calls
export const employeeAPI = {
  getAll: () => api.get('/employees'),
  getById: (id) => api.get(`/employees/${id}`),
  create: (data) => api.post('/employees', data),
};

// Attendance API calls
export const attendanceAPI = {
  getAll: (params) => api.get('/attendance', { params }),
  checkIn: (employeeId) => api.post('/attendance/check-in', { employee_id: employeeId }),
  checkOut: (employeeId) => api.post('/attendance/check-out', { employee_id: employeeId }),
  update: (id, data) => api.put(`/attendance/${id}`, data),
};

// Department API calls
export const departmentAPI = {
  getAll: () => api.get('/departments'),
  create: (data) => api.post('/departments', data),
};

// Company API calls
export const companyAPI = {
  getAll: () => api.get('/companies'),
  create: (data) => api.post('/companies', data),
};

// Leave Request API calls
export const leaveRequestAPI = {
  getAll: (params) => api.get('/leave-requests', { params }),
  create: (data) => api.post('/leave-requests', data),
  approve: (id) => api.post(`/leave-requests/${id}/approve`),
  reject: (id) => api.post(`/leave-requests/${id}/reject`),
};

// Statistics API calls
export const statisticsAPI = {
  getAttendance: () => api.get('/statistics/attendance'),
};

export default api;
