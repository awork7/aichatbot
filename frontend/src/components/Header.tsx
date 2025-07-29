import React from 'react';

interface HeaderProps {
  systemStatus: 'online' | 'offline' | 'loading';
}

const Header: React.FC<HeaderProps> = ({ systemStatus }) => {
  return (
    <div className="header-gradient p-6 rounded-2xl mb-6 shadow-xl">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <div className="logo-container">
            <div className="logo-icon">✨</div>
          </div>
          <div>
            <h1 className="main-title">Spark AI Assistant</h1>
            <p className="subtitle">South Indian Bank's Intelligent Banking Companion</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="sib-logo">🏦</div>
          <div className={`status-badge ${systemStatus}`}>
            <div className="status-dot"></div>
            {systemStatus === 'online' ? 'System Online' : 
             systemStatus === 'offline' ? 'System Offline' : 'Connecting...'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;
