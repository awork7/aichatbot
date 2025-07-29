import { useState, useCallback, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import apiService from '../services/api';
import { Message, ChatRequest } from '../types';

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => uuidv4());
  const [systemStatus, setSystemStatus] = useState<'online' | 'offline' | 'loading'>('loading');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check system health
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await apiService.getHealthStatus();
        setSystemStatus('online');
      } catch {
        setSystemStatus('offline');
      }
    };
    
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Initialize with welcome message
  useEffect(() => {
    setMessages([{
      id: '1',
      role: 'assistant',
      content: '🏦 **Welcome to Spark - South Indian Bank AI Assistant!**\n\nHello! I\'m here to help you with all your South Indian Bank needs. Ask me about accounts, loans, credit cards, or any other banking services!\n\n✨ *How can I assist you today?*',
      timestamp: new Date(),
    }]);
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isLoading) return;

    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const request: ChatRequest = {
        message: content.trim(),
        session_id: sessionId,
      };

      const response = await apiService.sendMessage(request);

      const assistantMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        response_time: response.response_time,
        timestamp: new Date(response.timestamp),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err: any) {
      const errorMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: '🚨 Sorry, I encountered an error. Please try again or check if the API server is running.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, isLoading]);

  const clearChat = useCallback(() => {
    setMessages([{
      id: '1',
      role: 'assistant',
      content: '🏦 **Chat cleared!** How can I help you with South Indian Bank services today?',
      timestamp: new Date(),
    }]);
  }, []);

  return {
    messages,
    isLoading,
    sendMessage,
    clearChat,
    sessionId,
    messagesEndRef,
    systemStatus
  };
};
