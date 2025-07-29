import React, { useState } from 'react';
import { useChat } from '../hooks/useChat';

const ChatInterface: React.FC = () => {
  const [inputMessage, setInputMessage] = useState('');
  const { messages, isLoading, sendMessage, clearChat, messagesEndRef } = useChat();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputMessage.trim() && !isLoading) {
      sendMessage(inputMessage);
      setInputMessage('');
    }
  };

  const quickSuggestions = [
    "What services does SIB offer?",
    "How do I open a savings account?",
    "Tell me about home loans",
    "What are the interest rates?"
  ];

  return (
    <div className="chat-interface">
      {/* Quick Suggestions */}
      <div className="quick-suggestions">
        {quickSuggestions.map((suggestion, index) => (
          <button
            key={index}
            className="suggestion-chip"
            onClick={() => setInputMessage(suggestion)}
          >
            {suggestion}
          </button>
        ))}
      </div>

      {/* Messages Area */}
      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.role}`}>
            <div className="message-avatar">
              {message.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
              <div className="message-bubble">
                {message.content.split('\n').map((line, index) => (
                  <div key={index} className="message-line">
                    {line.startsWith('**') && line.endsWith('**') ? (
                      <strong>{line.slice(2, -2)}</strong>
                    ) : line.startsWith('*') && line.endsWith('*') ? (
                      <em>{line.slice(1, -1)}</em>
                    ) : (
                      <span>{line}</span>
                    )}
                  </div>
                ))}
              </div>
              
              {/* Message metadata */}
              <div className="message-meta">
                <span>{message.timestamp.toLocaleTimeString()}</span>
                {message.response_time && (
                  <span>• {message.response_time.toFixed(1)}s</span>
                )}
              </div>

              {/* Sources */}
              {message.sources && message.sources.length > 0 && (
                <div className="message-sources">
                  <div className="sources-title">📚 Sources:</div>
                  {message.sources.map((source, index) => (
                    <div key={index} className="source-item">📄 {source}</div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="typing-indicator">
                <div className="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span className="typing-text">Spark is thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="input-area">
        <form onSubmit={handleSubmit} className="input-form">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask me about South Indian Bank services..."
            disabled={isLoading}
            rows={1}
            className="message-input"
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
          
          <div className="input-actions">
            <button
              type="button"
              onClick={clearChat}
              disabled={isLoading}
              className="clear-btn"
              title="Clear chat"
            >
              🔄
            </button>
            
            <button
              type="submit"
              disabled={!inputMessage.trim() || isLoading}
              className="send-btn"
            >
              {isLoading ? '⏳' : '🚀'}
            </button>
          </div>
        </form>
        
        <div className="input-help">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
