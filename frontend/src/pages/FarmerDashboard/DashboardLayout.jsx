// src/pages/FarmerDashboard/DashboardLayout.jsx
import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import './DashboardLayout.css';

const DashboardLayout = () => {
  return (
    <div className="dashboard-layout">
      <aside className="dashboard-sidebar">
        <nav>
          <NavLink to="/dashboard/my-listings">My Listings</NavLink>
          <NavLink to="/dashboard/orders">Manage Orders</NavLink>
          <NavLink to="/dashboard/add-produce">Add New Produce</NavLink>
        </nav>
      </aside>
      <main className="dashboard-content">
        <Outlet /> {/* This will render the nested route component */}
      </main>
    </div>
  );
};

export default DashboardLayout;
