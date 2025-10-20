// src/components/specific/ProduceCard.jsx
import React from 'react';
import { useDispatch } from 'react-redux';
import { addToCart } from '../../features/cart/cartSlice';
import { FaMapMarkerAlt } from 'react-icons/fa';
import Swal from 'sweetalert2';
import './ProduceCard.css';

const ProduceCard = ({ produce }) => {
  const dispatch = useDispatch();
  const { name, price, unit, image_url, location } = produce;
  const placeholderImage = 'https://via.placeholder.com/300x200.png?text=No+Image';

  const handleAddToCart = () => {
    dispatch(addToCart(produce));
    Swal.fire({
      toast: true,
      icon: 'success',
      title: `${name} added to cart!`,
      position: 'top-end',
      showConfirmButton: false,
      timer: 1500,
      timerProgressBar: true,
    });
  };

  return (
    <div className="produce-card">
      <img src={image_url || placeholderImage} alt={name} className="produce-image" />
      <div className="produce-info">
        <h3 className="produce-name">{name}</h3>
        <p className="produce-price">
          KES {price} / {unit}
        </p>
        {location && (
          <p className="produce-location">
            <FaMapMarkerAlt /> {location}
          </p>
        )}
        <button onClick={handleAddToCart} className="add-to-cart-btn">
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default ProduceCard;