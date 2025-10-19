// src/pages/FarmerDashboard/MyListings.jsx
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMyProduce, deleteProduce } from '../../features/produce/produceSlice';
import { Link } from 'react-router-dom';
import { FaEdit, FaTrash } from 'react-icons/fa';
import Swal from 'sweetalert2';
import './MyListings.css';

const MyListings = () => {
  const dispatch = useDispatch();

  // --- THIS IS THE FIX ---
  // Provide a default empty object to prevent destructuring undefined
  const { myItems, isLoading } = useSelector((state) => state.produce) || {};

  useEffect(() => {
    dispatch(fetchMyProduce());
  }, [dispatch]);

  const handleDelete = (produceId, produceName) => {
    Swal.fire({
      title: 'Are you sure?',
      text: `You are about to delete "${produceName}". You won't be able to revert this!`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Yes, delete it!',
    }).then((result) => {
      if (result.isConfirmed) {
        dispatch(deleteProduce(produceId)).then((action) => {
          if (deleteProduce.fulfilled.match(action)) {
            Swal.fire('Deleted!', 'Your produce has been deleted.', 'success');
          }
        });
      }
    });
  };

  if (isLoading) {
    return <p>Loading your listings...</p>;
  }

  return (
    <div className="my-listings-container">
      <div className="header">
        <h2>My Produce Listings</h2>
        <Link to="/dashboard/add-produce" className="add-new-btn">
          + Add New Produce
        </Link>
      </div>

      {myItems && myItems.length > 0 ? ( // Added defensive check for myItems
        <table className="listings-table">
          <thead>
            <tr>
              <th>Image</th>
              <th>Name</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {myItems.map((item) => (
              <tr key={item.id}>
                <td>
                  <img src={item.image_url || 'https://via.placeholder.com/80'} alt={item.name} className="item-image" />
                </td>
                <td>{item.name}</td>
                <td>{item.price} / {item.unit}</td>
                <td>{item.quantity}</td>
                <td>{item.is_available ? <span className="status available">Available</span> : <span className="status sold-out">Sold Out</span>}</td>
                <td className="actions">
                  <button className="action-btn edit-btn"><FaEdit /> Edit</button>
                  <button onClick={() => handleDelete(item.id, item.name)} className="action-btn delete-btn"><FaTrash /> Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div className="no-listings">
          <p>You have not listed any produce yet.</p>
          <Link to="/dashboard/add-produce" className="add-new-btn">List Your First Item</Link>
        </div>
      )}
    </div>
  );
};

export default MyListings;