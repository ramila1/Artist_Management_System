import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/',  // Adjust URL as per your Django API
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});

axiosInstance.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Handle token expiration or unauthorized access
      console.error('Unauthorized! Please login again.');
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
