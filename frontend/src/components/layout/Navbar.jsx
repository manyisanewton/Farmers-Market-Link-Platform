// src/components/layout/Navbar.jsx
import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../../features/auth/authSlice';
import { FaLeaf, FaShoppingCart, FaTachometerAlt } from 'react-icons/fa';
import './Navbar.css';

const Navbar = () => {
  // Get full authentication state, providing a default to prevent errors on initial load
  const { isAuthenticated, user } = useSelector((state) => state.auth) || {};
  
  // Get cart items state defensively
  const cartItems = useSelector((state) => state.cart?.cartItems) || [];
  
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <NavLink to="/" className="navbar-logo">
          <FaLeaf className="logo-icon" />
          FMLP
        </NavLink>
        <ul className="nav-menu">
          <li className="nav-item">
            <NavLink to="/market" className="nav-links">
              Marketplace
            </NavLink>
          </li>
          
          {/* --- REAL ROLE CHECK --- */}
          {/* Conditional Dashboard Link: Shows only if the user is authenticated and their role is 'farmer' */}
          {isAuthenticated && user?.role === 'farmer' && (
            <li className="nav-item">
              <NavLink to="/dashboard/my-listings" className="nav-links">
                <FaTachometerAlt /> Dashboard
              </NavLink>
            </li>
          )}
          {/* We can add a similar link for `user?.role === 'admin'` here in the future */}


          {isAuthenticated ? (
            <>
              {/* Cart Icon */}
              <li className="nav-item">
                <NavLink to="/cart" className="nav-links">
                  <FaShoppingCart />
                  {cartItems.length > 0 && (
                    <span className="cart-badge">{cartItems.length}</span>
                  )}
                </NavLink>
              </li>
              {/* Logout Button */}
              <li className="nav-item">
                <button onClick={handleLogout} className="nav-links-button">
                  Logout
                </button>
              </li>
            </>
          ) : (
            <>
              {/* Login and Sign Up Links for logged-out users */}
              <li className="nav-item">
                <NavLink to="/login" className="nav-links">
                  Login
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink to="/register" className="nav-links-button">
                  Sign Up
                </NavLink>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;