// src/routes/AppRoutes.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';

// Public Page Imports
import HomePage from '../pages/HomePage';
import LoginPage from '../pages/LoginPage';
import RegisterPage from '../pages/RegisterPage';
import MarketplacePage from '../pages/MarketplacePage';
import CartPage from '../pages/CartPage';

// Protected Route and Layout Imports
import ProtectedRoute from './ProtectedRoute';
import DashboardLayout from '../pages/FarmerDashboard/DashboardLayout';
import AdminDashboard from '../pages/AdminDashboard/AdminDashboard'; // Import AdminDashboard

// Farmer Dashboard Page Imports
import MyListings from '../pages/FarmerDashboard/MyListings';
import ManageOrders from '../pages/FarmerDashboard/ManageOrders';
import AddProduce from '../pages/FarmerDashboard/AddProduce';

const AppRoutes = () => {
  return (
    <Routes>
      {/* === Public Routes === */}
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/market" element={<MarketplacePage />} />
      
      {/* === General Protected Routes === */}
      <Route 
        path="/cart" 
        element={
          <ProtectedRoute allowedRoles={['buyer', 'farmer', 'admin']}>
            <CartPage />
          </ProtectedRoute>
        } 
      />

      {/* === Farmer Dashboard Nested Routes === */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute allowedRoles={['farmer']}>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route path="my-listings" element={<MyListings />} />
        <Route path="orders" element={<ManageOrders />} />
        <Route path="add-produce" element={<AddProduce />} />
        {/* Optional: Add a default child route for /dashboard */}
        <Route index element={<MyListings />} /> 
      </Route>

      {/* === Admin Routes === */}
      <Route
        path="/admin/dashboard"
        element={
          <ProtectedRoute allowedRoles={['admin']}>
            <AdminDashboard />
          </ProtectedRoute>
        }
      />

      {/* 404 Not Found page */}
      <Route path="*" element={<div>404 Not Found</div>} />
    </Routes>
  );
};

export default AppRoutes;