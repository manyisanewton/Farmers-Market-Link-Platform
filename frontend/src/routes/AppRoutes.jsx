// src/routes/AppRoutes.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import LoginPage from '../pages/LoginPage';
import RegisterPage from '../pages/RegisterPage';
import MarketplacePage from '../pages/MarketplacePage';
import AddProduce from '../pages/FarmerDashboard/AddProduce'; // Import the new component

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/market" element={<MarketplacePage />} />

      {/* Farmer Routes (will be protected later) */}
      <Route path="/dashboard/add-produce" element={<AddProduce />} />
    </Routes>
  );
};

export default AppRoutes;