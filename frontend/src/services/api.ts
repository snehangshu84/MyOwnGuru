import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1'

export const api = axios.create({ baseURL })

// Attach bearer token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers = config.headers || {}
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})
