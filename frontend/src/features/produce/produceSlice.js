// src/features/produce/produceSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../api/axiosInstance';

// Async thunk for fetching produce
export const fetchProduce = createAsyncThunk(
  'produce/fetchProduce',
  async (filters = {}, { rejectWithValue }) => {
    try {
      // The filters object will be converted to query parameters
      const response = await axiosInstance.get('/produce/', { params: filters });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  items: [],
  isLoading: false,
  error: null,
};

const produceSlice = createSlice({
  name: 'produce',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
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
      });
  },
});

export default produceSlice.reducer;