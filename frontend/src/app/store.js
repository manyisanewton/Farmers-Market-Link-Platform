import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../features/auth/authSlice';
import produceReducer from '../features/produce/produceSlice';
import cartReducer from '../features/cart/cartSlice'; 
import orderReducer from '../features/orders/orderSlice';
import adminReducer from '../features/admin/adminSlice';


export const store = configureStore({
  reducer: {
    auth: authReducer,
    produce: produceReducer,
    cart: cartReducer,
    orders: orderReducer,
    admin: adminReducer,
  },
});