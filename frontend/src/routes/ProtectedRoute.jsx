import React from 'react';
import { useSelector } from 'react-redux';
import { Navigate, useLocation } from 'react-router-dom';
import Swal from 'sweetalert2';

// This component will wrap our protected routes
const ProtectedRoute = ({ children, allowedRoles }) => {
  const { isAuthenticated, user } = useSelector((state) => state.auth);
  const location = useLocation();

  if (!isAuthenticated) {
    // If user is not logged in, redirect them to the login page
    // state={{ from: location }} preserves the page they were trying to access
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // In a real app, user role would come from decoding the JWT or a /me endpoint
  // For now, we'll simulate it. Let's assume we decode the token to get the role.
  // We need to implement this logic in authSlice later.
  const userRole = 'farmer'; // <<< --- THIS IS A TEMPORARY SIMULATION

  if (!allowedRoles.includes(userRole)) {
    // If the user's role is not allowed, show an alert and redirect
    Swal.fire({
      icon: 'error',
      title: 'Access Denied',
      text: 'You do not have permission to view this page.',
    });
    // Redirect to a safe page, like the marketplace
    return <Navigate to="/market" replace />;
  }

  // If authenticated and role is allowed, render the child component
  return children;
};

export default ProtectedRoute;