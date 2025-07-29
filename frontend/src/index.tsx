import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';  // Import Tailwind here
import App from './App.tsx';  // Add .tsx extension explicitly


const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
