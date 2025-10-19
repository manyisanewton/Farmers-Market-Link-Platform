// src/pages/LoginPage.jsx
import React, { useState } from 'react'; // <-- FIX: Import useState
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../features/auth/authSlice';
import Swal from 'sweetalert2';
import './LoginPage.css';

const LoginPage = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const { isLoading } = useSelector((state) => state.auth);
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

    const resultAction = await dispatch(loginUser(formData));
    if (loginUser.fulfilled.match(resultAction)) {
      Swal.fire({
        icon: 'success',
        title: 'Logged In!',
        text: 'Welcome back.',
        timer: 2000,
        showConfirmButton: false,
      });
      navigate('/market');
    }
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