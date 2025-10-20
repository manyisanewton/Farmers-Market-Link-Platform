import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchFarmerOrders, updateOrderStatus } from '../../features/orders/orderSlice';
import './ManageOrders.css';

const ManageOrders = () => {
  const dispatch = useDispatch();
  const { orders, isLoading } = useSelector((state) => state.orders) || { orders: [], isLoading: false };

  useEffect(() => {
    dispatch(fetchFarmerOrders());
  }, [dispatch]);

  const handleStatusChange = (orderId, newStatus) => {
    dispatch(updateOrderStatus({ orderId, status: newStatus }));
  };

  if (isLoading) {
    return <p>Loading orders...</p>;
  }

  return (
    <div className="manage-orders-container">
      <h2>Incoming Orders</h2>
      {orders.length > 0 ? (
        <div className="orders-list">
          {orders.map(order => (
            <div key={order.id} className={`order-card status-${order.status.toLowerCase()}`}>
              <div className="order-header">
                <h3>Order #{order.id}</h3>
                <span className={`status-badge status-${order.status.toLowerCase()}`}>{order.status}</span>
              </div>
              <div className="order-body">
                <p><strong>Date:</strong> {new Date(order.created_at).toLocaleDateString()}</p>
                <p><strong>Total Price:</strong> KES {order.total_price}</p>
                <h4>Items:</h4>
                <ul>
                  {order.order_items.map(item => (
                    <li key={item.produce.id}>
                      {item.quantity} {item.produce.unit} of {item.produce.name}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="order-actions">
                <span>Update Status:</span>
                <select 
                  defaultValue={order.status}
                  onChange={(e) => handleStatusChange(order.id, e.target.value)}
                >
                  <option value="Pending">Pending</option>
                  <option value="Confirmed">Confirmed</option>
                  <option value="Delivered">Delivered</option>
                  <option value="Canceled">Canceled</option>
                </select>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p>You have no incoming orders at the moment.</p>
      )}
    </div>
  );
};

export default ManageOrders;