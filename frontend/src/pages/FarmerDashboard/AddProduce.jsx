import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../../api/axiosInstance';
import Swal from 'sweetalert2';
import './AddProduce.css';

const AddProduce = () => {
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    quantity: '',
    unit: 'kg',
    location: '',
    description: '',
  });
  const [imageFile, setImageFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setImageFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    // Create a FormData object to handle file upload
    const submissionData = new FormData();
    // Append all text fields from state to the FormData
    for (const key in formData) {
      submissionData.append(key, formData[key]);
    }
    // Append the image file if it exists
    if (imageFile) {
      submissionData.append('image', imageFile);
    }

    try {
      await axiosInstance.post('/produce/', submissionData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      Swal.fire({
        icon: 'success',
        title: 'Produce Added!',
        text: `${formData.name} has been successfully listed on the marketplace.`,
      });
      
      // TODO: Navigate to the 'My Listings' page once it's created. For now, we can go to the market.
      navigate('/market');

    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Submission Failed',
        text: error.response?.data?.message || 'There was an error listing your produce.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="add-produce-container">
      <form className="add-produce-form" onSubmit={handleSubmit}>
        <h2>Add New Produce</h2>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="name">Produce Name</label>
            <input type="text" id="name" name="name" value={formData.name} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="location">Location (County)</label>
            <input type="text" id="location" name="location" value={formData.location} onChange={handleChange} required />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="price">Price (KES)</label>
            <input type="number" id="price" name="price" value={formData.price} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="quantity">Quantity</label>
            <input type="number" id="quantity" name="quantity" value={formData.quantity} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="unit">Unit</label>
            <select id="unit" name="unit" value={formData.unit} onChange={handleChange}>
              <option value="kg">Per Kg</option>
              <option value="bunch">Per Bunch</option>
              <option value="crate">Per Crate</option>
              <option value="item">Per Item</option>
            </select>
          </div>
        </div>
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea id="description" name="description" value={formData.description} onChange={handleChange} rows="4"></textarea>
        </div>
        <div className="form-group">
          <label htmlFor="image">Produce Image</label>
          <input type="file" id="image" name="image" onChange={handleFileChange} accept="image/*" />
        </div>
        <button type="submit" className="submit-btn" disabled={isLoading}>
          {isLoading ? 'Submitting...' : 'Add Produce'}
        </button>
      </form>
    </div>
  );
};

export default AddProduce;