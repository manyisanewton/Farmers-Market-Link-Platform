import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="home-container">
      <header className="home-hero">
        <h1>Welcome to the Farmers' Market Link Platform</h1>
        <p>Connecting Farmers Directly to Buyers</p>
        <div className="hero-buttons">
          <Link to="/market" className="hero-button primary">
            Browse Marketplace
          </Link>
          <Link to="/register" className="hero-button secondary">
            Join as a Farmer
          </Link>
        </div>
      </header>
    </div>
  );
};

export default HomePage;