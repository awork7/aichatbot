import React, { useEffect, useState } from 'react';
import apiService from '../services/api';
import { ServiceInfo } from '../types';

interface SidebarProps {
  onServiceClick: (service: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onServiceClick }) => {
  const [services, setServices] = useState<ServiceInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await apiService.getBankingServices();
        setServices(response.services);
      } catch (error) {
        console.error('Failed to fetch services:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchServices();
  }, []);

  const handleServiceClick = (serviceName: string) => {
    onServiceClick(`Tell me about ${serviceName}`);
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2 className="sidebar-title">Banking Services</h2>
        <p className="sidebar-subtitle">Click on any service to learn more</p>
      </div>

      <div className="status-card">
        <div className="status-indicator">
          <div className="status-online">
            <div className="pulse-dot"></div>
            SYSTEM ONLINE
          </div>
        </div>
        <div className="metrics-grid">
          <div className="metric">
            <div className="metric-value">99.9%</div>
            <div className="metric-label">Uptime</div>
          </div>
          <div className="metric">
            <div className="metric-value">< 8s</div>
            <div className="metric-label">Response</div>
          </div>
        </div>
      </div>

      <div className="services-list">
        {loading ? (
          <div className="loading-spinner">Loading...</div>
        ) : (
          services.map((service) => (
            <div
              key={service.id}
              className="service-card"
              onClick={() => handleServiceClick(service.name)}
            >
              <div className="service-icon">{service.icon}</div>
              <div className="service-info">
                <div className="service-name">{service.name}</div>
                {service.description && (
                  <div className="service-description">{service.description}</div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="sidebar-footer">
        <div className="footer-text">
          🏦 Powered by Spark AI<br />
          South Indian Bank © 2025
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
