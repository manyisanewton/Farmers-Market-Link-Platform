import React from 'react';
import { FaMapMarkerAlt } from 'react-icons/fa';
import './ProduceCard.css';

const ProduceCard = ({ produce }) => {
  const { name, price, unit, image_url, location, farmer } = produce;
  const placeholderImage = 'https://via.placeholder.com/300x200.png?text=No+Image';

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
        {/* In a later step, we can add farmer info here */}
        <button className="add-to-cart-btn">Add to Cart</button>
      </div>
    </div>
  );
};

export default ProduceCard;