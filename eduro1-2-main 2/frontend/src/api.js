import axios from 'axios';

const getApiUrl = () => {
  if (window.location.hostname === 'localhost') {
    return 'http://localhost:8000/api';
  }
  // For Compyle preview - both ports use same base domain
  const hostname = window.location.hostname;
  const port = window.location.port;

  if (port === '3001') {
    return `${window.location.protocol}//${hostname.replace(/:\d+$/, '')}:8000/api`;
  }
  return `${window.location.protocol}//${hostname}/api`;
};

const API_URL = getApiUrl();
console.log('API URL:', API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (userType, email, password) => {
  const response = await api.post(`/auth/${userType}/login`, { email, password });
  return response.data;
};

export const getDashboardStats = async (userType) => {
  // Mock data for now since dashboard APIs aren't implemented yet
  return {
    admin: {
      total_students: 50,
      total_teachers: 10,
      avg_attendance: 85.5,
      upcoming_events: 3,
      attendance_trends: {
        dates: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        percentages: [85, 87, 83, 86, 88],
      },
      result_distribution: {
        pass_count: 45,
        fail_count: 5,
      },
    },
    teacher: {
      total_students: 45,
      avg_attendance: 87.2,
      pending_results: 5,
      subjects: [
        { id: 1, code: 'CS301', name: 'Data Structures' },
        { id: 2, code: 'CS302', name: 'Database Systems' },
      ],
    },
    student: {
      overall_attendance: 82.5,
      avg_percentage: 78.3,
      overall_grade: 'B+',
      subjects: [
        { subject_name: 'Data Structures', present_count: 38, total_count: 42, percentage: 90.5 },
        { subject_name: 'Database Systems', present_count: 35, total_count: 42, percentage: 83.3 },
      ],
      results: [
        { subject_name: 'Data Structures', internal_marks: 25, external_marks: 60, total_marks: 85, grade: 'A' },
        { subject_name: 'Database Systems', internal_marks: 23, external_marks: 55, total_marks: 78, grade: 'B+' },
      ],
    },
  }[userType] || {};
};

export default api;
