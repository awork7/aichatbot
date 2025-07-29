export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  timestamp: Date;
  response_time?: number;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
}

export interface ChatResponse {
  answer: string;
  sources: string[];
  response_time: number;
  session_id: string;
  timestamp: string;
}

export interface ServiceInfo {
  id: number;
  name: string;
  description?: string;
  icon: string;
  category: string;
}
