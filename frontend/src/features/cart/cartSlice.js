import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../api/axiosInstance';
import Swal from 'sweetalert2';

// Async thunk for submitting the order
export const submitOrder = createAsyncThunk(
  'cart/submitOrder',
  async (cartItems, { dispatch, rejectWithValue }) => {
    // Format the data for the backend API
    const orderData = {
      items: cartItems.map(item => ({
        produce_id: item.id,
        quantity: item.cartQuantity,
      })),
    };
    try {
      const response = await axiosInstance.post('/orders/', orderData);
      // On success, clear the cart
      dispatch(clearCart());
      return response.data; // The newly created order object
    } catch (error) {
      Swal.fire('Order Failed', error.response?.data?.message || 'An unexpected error occurred.', 'error');
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  cartItems: [],
  status: 'idle', // for tracking the submitOrder async thunk
  error: null,
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addToCart: (state, action) => {
      const item = action.payload;
      const existingItem = state.cartItems.find((i) => i.id === item.id);
      if (existingItem) {
        existingItem.cartQuantity += 1;
      } else {
        state.cartItems.push({ ...item, cartQuantity: 1 });
      }
    },
    removeFromCart: (state, action) => {
      const itemId = action.payload;
      state.cartItems = state.cartItems.filter((i) => i.id !== itemId);
    },
    updateQuantity: (state, action) => {
      const { id, quantity } = action.payload;
      const item = state.cartItems.find((i) => i.id === id);
      if (item) {
        item.cartQuantity = quantity;
      }
    },
    clearCart: (state) => {
      state.cartItems = [];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(submitOrder.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(submitOrder.fulfilled, (state) => {
        state.status = 'succeeded';
      })
      .addCase(submitOrder.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      });
  },
});

export const { addToCart, removeFromCart, updateQuantity, clearCart } = cartSlice.actions;

export default cartSlice.reducer;