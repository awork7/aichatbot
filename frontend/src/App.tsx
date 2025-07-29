import React, { useState } from 'react';
import './App.css';

const App: React.FC = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Array<{id: number, text: string, isUser: boolean}>>([
    { id: 1, text: "🏦 Welcome to Spark - South Indian Bank AI Assistant! How can I help you today?", isUser: false }
  ]);

  const sendMessage = () => {
    if (!message.trim()) return;
    
    // Add user message
    const newMessages = [...messages, { id: Date.now(), text: message, isUser: true }];
    setMessages(newMessages);
    setMessage('');
    
    // Simulate AI response (you'll replace this with real API calls later)
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        id: Date.now(), 
        text: "Thanks for your message! I'm ready to help with South Indian Bank services.", 
        isUser: false 
      }]);
    }, 1000);
  };

  return (
    <div style={{
      height: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      flexDirection: 'column',
      fontFamily: 'Arial, sans-serif'
    }}>
      {/* Header */}
      <div style={{
        background: 'rgba(255,255,255,0.1)',
        padding: '20px',
        color: 'white',
        textAlign: 'center',
        backdropFilter: 'blur(10px)'
      }}>
        <h1 style={{margin: 0, fontSize: '2.5rem'}}>✨ Spark AI Assistant</h1>
        <p style={{margin: '10px 0 0 0', opacity: 0.9}}>South Indian Bank's Intelligent Banking Companion</p>
      </div>

      {/* Messages Area */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '15px'
      }}>
        {messages.map(msg => (
          <div key={msg.id} style={{
            display: 'flex',
            justifyContent: msg.isUser ? 'flex-end' : 'flex-start'
          }}>
            <div style={{
              background: msg.isUser 
                ? 'linear-gradient(135deg, #3b82f6, #8b5cf6)' 
                : 'rgba(255,255,255,0.9)',
              color: msg.isUser ? 'white' : '#333',
              padding: '15px 20px',
              borderRadius: '20px',
              maxWidth: '70%',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
            }}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      {/* Input Area */}
      <div style={{
        padding: '20px',
        background: 'rgba(255,255,255,0.1)',
        backdropFilter: 'blur(10px)'
      }}>
        <div style={{
          display: 'flex',
          gap: '10px',
          background: 'rgba(255,255,255,0.9)',
          borderRadius: '25px',
          padding: '10px'
        }}>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask me about South Indian Bank services..."
            style={{
              flex: 1,
              border: 'none',
              outline: 'none',
              padding: '10px 15px',
              fontSize: '16px',
              borderRadius: '20px',
              background: 'transparent'
            }}
          />
          <button
            onClick={sendMessage}
            style={{
              background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
              color: 'white',
              border: 'none',
              borderRadius: '50%',
              width: '50px',
              height: '50px',
              cursor: 'pointer',
              fontSize: '20px'
            }}
          >
            🚀
          </button>
        </div>
      </div>
    </div>
  );
};

export default App;
