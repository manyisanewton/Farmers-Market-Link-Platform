// src/pages/RegisterPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../api/axiosInstance';
import Swal from 'sweetalert2';
import './RegisterPage.css'; // We'll share some styles with the login page

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    phone_number: '',
    password: '',
    role: 'buyer', // Default role
  });
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await axiosInstance.post('/auth/register', formData);
      Swal.fire({
        icon: 'success',
        title: 'Registration Successful!',
        text: 'You can now log in.',
        timer: 3000,
        showConfirmButton: false,
      });
      navigate('/login'); // Redirect to login page after successful registration
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Registration Failed',
        text: error.response?.data?.message || 'An unknown error occurred. Please try again.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-container">
      <form className="register-form" onSubmit={handleSubmit}>
        <h2>Create an Account</h2>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input type="text" id="username" name="username" value={formData.username} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input type="email" id="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="phone_number">Phone Number</label>
          <input type="tel" id="phone_number" name="phone_number" value={formData.phone_number} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input type="password" id="password" name="password" value={formData.password} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="role">Register as a:</label>
          <select id="role" name="role" value={formData.role} onChange={handleChange}>
            <option value="buyer">Buyer (Hotel, Retailer, etc.)</option>
            <option value="farmer">Farmer (Producer)</option>
          </select>
        </div>
        <button type="submit" className="register-button" disabled={isLoading}>
          {isLoading ? 'Registering...' : 'Register'}
        </button>
        <p className="login-link">
          Already have an account? <a href="/login">Login here</a>
        </p>
      </form>
    </div>
  );
};

export default RegisterPage;