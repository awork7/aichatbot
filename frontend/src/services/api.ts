import axios from 'axios';
import { ChatRequest, ChatResponse, ServiceInfo } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class SIBApiService {
  private api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 60000,
    headers: { 'Content-Type': 'application/json' },
  });

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await this.api.post('/api/v1/chat/message', request);
    return response.data;
  }

  async getHealthStatus() {
    const response = await this.api.get('/health');
    return response.data;
  }

  async getBankingServices(): Promise<{ services: ServiceInfo[]; total: number }> {
    const response = await this.api.get('/api/v1/services/');
    return response.data;
  }
}

export default new SIBApiService();
