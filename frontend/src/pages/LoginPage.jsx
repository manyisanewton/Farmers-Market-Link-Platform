// src/pages/LoginPage.jsx
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../features/auth/authSlice';
import Swal from 'sweetalert2';
import './LoginPage.css';

const LoginPage = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  // Get isLoading state defensively, falling back to false
  const isLoading = useSelector((state) => state.auth?.isLoading) || false;
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.email || !formData.password) {
      return Swal.fire({
        icon: 'warning',
        title: 'Oops...',
        text: 'Please fill in all fields!',
      });
    }

    // Dispatch the login action and wait for it to complete
    const resultAction = await dispatch(loginUser(formData));
    
    // Check if the action was fulfilled (i.e., successful)
    if (loginUser.fulfilled.match(resultAction)) {
      // The payload is now guaranteed to be { access_token, user }
      const user = resultAction.payload.user;

      Swal.fire({
        icon: 'success',
        title: 'Logged In!',
        text: `Welcome back, ${user.username}!`,
        timer: 1500,
        showConfirmButton: false,
      });

      // Perform redirection based on the user's role
      if (user.role === 'admin') {
        navigate('/admin/dashboard');
      } else if (user.role === 'farmer') {
        navigate('/dashboard/my-listings');
      } else {
        // Default for buyers
        navigate('/market');
      }
    }
    // No 'else' block needed, as the loginUser thunk handles showing the error alert on failure
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Login to FMLP</h2>
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input
            type="email" id="email" name="email"
            value={formData.email} onChange={handleChange} required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password" id="password" name="password"
            value={formData.password} onChange={handleChange} required
          />
        </div>
        <button type="submit" className="login-button" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
        <p className="register-link">
          Don't have an account? <a href="/register">Register here</a>
        </p>
      </form>
    </div>
  );
};

export default LoginPage;