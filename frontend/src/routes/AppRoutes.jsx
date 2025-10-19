import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import LoginPage from '../pages/LoginPage';
import RegisterPage from '../pages/RegisterPage';
import MarketplacePage from '../pages/MarketplacePage';
import AddProduce from '../pages/FarmerDashboard/AddProduce';
import MyListings from '../pages/FarmerDashboard/MyListings'; // Import MyListings
import ProtectedRoute from './ProtectedRoute'; // Import ProtectedRoute

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/market" element={<MarketplacePage />} />

      {/* Farmer Routes - Wrapped in ProtectedRoute */}
      <Route
        path="/dashboard/my-listings"
        element={
          <ProtectedRoute allowedRoles={['farmer']}>
            <MyListings />
          </ProtectedRoute>
        }
      />
      <Route
        path="/dashboard/add-produce"
        element={
          <ProtectedRoute allowedRoles={['farmer']}>
            <AddProduce />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default AppRoutes;