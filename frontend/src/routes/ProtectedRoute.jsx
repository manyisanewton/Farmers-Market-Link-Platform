// src/routes/ProtectedRoute.jsx
import React from 'react';
import { useSelector } from 'react-redux';
import { Navigate, useLocation } from 'react-router-dom';
import Swal from 'sweetalert2';

const ProtectedRoute = ({ children, allowedRoles }) => {
  // Get the full, real user object from the Redux state
  const { isAuthenticated, user } = useSelector((state) => state.auth);
  const location = useLocation();

  // 1. Check if the user is authenticated
  if (!isAuthenticated) {
    // If not, redirect to the login page, preserving the intended destination
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // 2. Check if the user object (with role) has been loaded yet
  // If we are authenticated but don't have the user role yet, it means
  // the fetchUserDetails thunk is still in flight. Show a loading state.
  if (!user || !user.role) {
    return <div>Loading user details...</div>; // Or a proper spinner component
  }

  // 3. Check if the loaded user's role is in the allowedRoles array
  if (!allowedRoles.includes(user.role)) {
    // If their role is not allowed, show an alert and redirect them.
    // Using a setTimeout to ensure the alert is visible before redirecting.
    setTimeout(() => {
      Swal.fire({
        icon: 'error',
        title: 'Access Denied',
        text: 'You do not have permission to view this page.',
      });
    }, 0);
    
    // Redirect to a safe, public page like the marketplace
    return <Navigate to="/market" replace />;
  }

  // 4. If all checks pass, render the protected component
  return children;
};

export default ProtectedRoute;