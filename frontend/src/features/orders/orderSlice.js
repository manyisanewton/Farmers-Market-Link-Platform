import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../api/axiosInstance';
import Swal from 'sweetalert2';

// Async thunk for fetching a farmer's incoming orders
export const fetchFarmerOrders = createAsyncThunk(
  'orders/fetchFarmerOrders',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axiosInstance.get('/orders/farmer');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const updateOrderStatus = createAsyncThunk(
  'orders/updateOrderStatus',
  async ({ orderId, status }, { rejectWithValue }) => {
    try {
      const response = await axiosInstance.patch(`/orders/${orderId}`, { status });
      return response.data;
    } catch (error) {
      Swal.fire('Update Failed', error.response?.data?.message || 'Could not update the order status.', 'error');
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  orders: [],
  isLoading: false,
  error: null,
};

const orderSlice = createSlice({
  name: 'orders',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchFarmerOrders.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchFarmerOrders.fulfilled, (state, action) => {
        state.isLoading = false;
        state.orders = action.payload;
      })
      .addCase(fetchFarmerOrders.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(updateOrderStatus.fulfilled, (state, action) => {
        // Find the index of the updated order and replace it
        const index = state.orders.findIndex(order => order.id === action.payload.id);
        if (index !== -1) {
          state.orders[index] = action.payload;
        }
      });
  },
});

export default orderSlice.reducer;