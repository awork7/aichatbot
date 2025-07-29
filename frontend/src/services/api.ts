import axios, { AxiosResponse } from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Make sure this matches your backend

class SIBApiService {
  private api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 60000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  constructor() {
    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('❌ API Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => {
        console.log('✅ API Response:', response.status, response.data);
        return response;
      },
      (error) => {
        console.error('❌ API Response Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  async sendMessage(message: string, sessionId?: string) {
    try {
      const response = await this.api.post('/api/v1/chat/message', {
        message,
        session_id: sessionId
      });
      return response.data;
    } catch (error: any) {
      console.error('❌ Send message error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to send message');
    }
  }

  async getHealthStatus() {
    try {
      const response = await this.api.get('/health');
      return response.data;
    } catch (error: any) {
      console.error('❌ Health check error:', error);
      throw new Error('Failed to get health status');
    }
  }

  async getBankingServices() {
    try {
      const response = await this.api.get('/api/v1/services/');
      return response.data;
    } catch (error: any) {
      console.error('❌ Get services error:', error);
      throw new Error('Failed to get banking services');
    }
  }
}

export default new SIBApiService();
