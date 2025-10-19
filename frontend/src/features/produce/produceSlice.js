// src/features/produce/produceSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../api/axiosInstance';
import Swal from 'sweetalert2';

// Async thunk for fetching all public produce listings
export const fetchProduce = createAsyncThunk(
  'produce/fetchProduce',
  async (filters = {}, { rejectWithValue }) => {
    try {
      const response = await axiosInstance.get('/produce/', { params: filters });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Async thunk for fetching ONLY the logged-in farmer's produce
export const fetchMyProduce = createAsyncThunk(
  'produce/fetchMyProduce',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axiosInstance.get('/produce/my-listings');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Async thunk for deleting a produce item
export const deleteProduce = createAsyncThunk(
  'produce/deleteProduce',
  async (produceId, { rejectWithValue }) => {
    try {
      await axiosInstance.delete(`/produce/${produceId}`);
      return produceId; // Return the ID on success for removal from state
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Deletion Failed',
        text: error.response?.data?.message || 'Could not delete the produce listing.',
      });
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  items: [],      // For the public marketplace
  myItems: [],    // For the farmer's own dashboard
  isLoading: false,
  error: null,
};

const produceSlice = createSlice({
  name: 'produce',
  initialState,
  reducers: {}, // Standard reducers can go here if needed
  extraReducers: (builder) => {
    builder
      // Cases for fetching all produce (Marketplace)
      .addCase(fetchProduce.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchProduce.fulfilled, (state, action) => {
        state.isLoading = false;
        state.items = action.payload;
      })
      .addCase(fetchProduce.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Cases for fetching farmer's own produce (My Listings)
      .addCase(fetchMyProduce.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchMyProduce.fulfilled, (state, action) => {
        state.isLoading = false;
        state.myItems = action.payload;
      })
      .addCase(fetchMyProduce.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })

      // Case for handling a successful deletion
      .addCase(deleteProduce.fulfilled, (state, action) => {
        const deletedId = action.payload;
        // Remove the item from both state arrays to keep them in sync
        state.items = state.items.filter(item => item.id !== deletedId);
        state.myItems = state.myItems.filter(item => item.id !== deletedId);
      });
  },
});

export default produceSlice.reducer;