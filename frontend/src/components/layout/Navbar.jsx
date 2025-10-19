import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../../features/auth/authSlice';
import { FaLeaf } from 'react-icons/fa'; // Example icon
import './Navbar.css';

const Navbar = () => {
  const { isAuthenticated } = useSelector((state) => state.auth);
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
          {/* We will add dashboard links here later */}

          {isAuthenticated ? (
            <li className="nav-item">
              <button onClick={handleLogout} className="nav-links-button">
                Logout
              </button>
            </li>
          ) : (
            <>
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