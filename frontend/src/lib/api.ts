import axios, { AxiosError } from 'axios'
import { toast } from 'sonner'

// Use relative URL in production, or VITE_API_URL for development
// When building for production, set VITE_API_URL to empty string or your backend URL
const API_BASE_URL = import.meta.env.VITE_API_URL || ''

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Define error response type
interface ErrorResponse {
  detail?: string
  message?: string
}

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ErrorResponse>) => {
    const message = error.response?.data?.detail || error.message || 'An error occurred'
    toast.error(message)
    return Promise.reject(error)
  }
)

// API functions
export const api = {
  // Products
  products: {
    list: async (params?: { page?: number; per_page?: number; status?: string; search?: string }) => {
      const response = await apiClient.get('/api/products', { params })
      return response.data
    },
    get: async (id: string) => {
      const response = await apiClient.get(`/api/products/${id}`)
      return response.data
    },
    create: async (data: any) => {
      const response = await apiClient.post('/api/products', data)
      return response.data
    },
    update: async (id: string, data: any) => {
      const response = await apiClient.put(`/api/products/${id}`, data)
      return response.data
    },
    delete: async (id: string) => {
      await apiClient.delete(`/api/products/${id}`)
    },
    renew: async (id: string, months: number) => {
      const response = await apiClient.post(`/api/products/${id}/renew?months=${months}`)
      return response.data
    },
    stats: async () => {
      const response = await apiClient.get('/api/products/stats')
      return response.data
    },
  },
  
  // Phone Registry
  phone: {
    check: async (phoneNumber: string) => {
      const response = await apiClient.post('/api/phone/check', { phone_number: phoneNumber })
      return response.data
    },
    register: async (phoneNumber: string, metadata?: any) => {
      const response = await apiClient.post('/api/phone/register', { phone_number: phoneNumber, metadata })
      return response.data
    },
    bulkRegister: async (phoneNumbers: string[], metadata?: any) => {
      const response = await apiClient.post('/api/phone/bulk-register', { phone_numbers: phoneNumbers, metadata })
      return response.data
    },
    cleanup: async () => {
      const response = await apiClient.delete('/api/phone/cleanup')
      return response.data
    },
  },
  
  // Health
  health: async () => {
    const response = await apiClient.get('/health')
    return response.data
  },
}
