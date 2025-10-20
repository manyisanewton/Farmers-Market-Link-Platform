// src/pages/CartPage.jsx
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { removeFromCart, updateQuantity, submitOrder } from '../features/cart/cartSlice';
import { Link, useNavigate } from 'react-router-dom';
import { FaTrash } from 'react-icons/fa';
import Swal from 'sweetalert2';
import './CartPage.css';

const CartPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { cartItems, status } = useSelector((state) => state.cart);

  const handleRemove = (id) => dispatch(removeFromCart(id));
  const handleQuantityChange = (id, quantity) => {
    if (quantity > 0) {
      dispatch(updateQuantity({ id, quantity: Number(quantity) }));
    }
  };

  const handleCheckout = () => {
    Swal.fire({
      title: 'Confirm Order',
      text: "Are you sure you want to place this order?",
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#4a7c59',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, place order!',
    }).then((result) => {
      if (result.isConfirmed) {
        dispatch(submitOrder(cartItems)).then(action => {
          if (submitOrder.fulfilled.match(action)) {
            const orderId = action.payload.id;
            Swal.fire('Order Placed!', `Your order #${orderId} has been successfully submitted.`, 'success');
            // We'll build the order tracking page next
            navigate(`/market`); 
          }
        });
      }
    });
  };

  const subtotal = cartItems.reduce((acc, item) => acc + item.price * item.cartQuantity, 0);

  return (
    <div className="cart-container">
      <h1>Your Shopping Cart</h1>
      {cartItems.length === 0 ? (
        <div className="empty-cart">
          <p>Your cart is currently empty.</p>
          <Link to="/market" className="browse-btn">Browse Produce</Link>
        </div>
      ) : (
        <>
          <div className="cart-items">
            {cartItems.map(item => (
              <div key={item.id} className="cart-item">
                <img src={item.image_url || 'https://via.placeholder.com/100'} alt={item.name} />
                <div className="item-details">
                  <h3>{item.name}</h3>
                  <p>KES {item.price} / {item.unit}</p>
                </div>
                <div className="item-actions">
                  <input
                    type="number"
                    value={item.cartQuantity}
                    onChange={(e) => handleQuantityChange(item.id, e.target.value)}
                    min="1"
                  />
                  <button onClick={() => handleRemove(item.id)} className="remove-btn">
                    <FaTrash />
                  </button>
                </div>
                <div className="item-total">
                  KES {(item.price * item.cartQuantity).toFixed(2)}
                </div>
              </div>
            ))}
          </div>
          <div className="cart-summary">
            <h2>Order Summary</h2>
            <div className="summary-row">
              <span>Subtotal</span>
              <span>KES {subtotal.toFixed(2)}</span>
            </div>
            <button onClick={handleCheckout} className="checkout-btn" disabled={status === 'loading'}>
              {status === 'loading' ? 'Placing Order...' : 'Proceed to Checkout'}
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default CartPage;