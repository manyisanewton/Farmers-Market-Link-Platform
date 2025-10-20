import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../api/axiosInstance';
import Swal from 'sweetalert2';

// Async thunk for fetching all users
export const fetchAllUsers = createAsyncThunk(
  'admin/fetchAllUsers',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axiosInstance.get('/admin/users');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Async thunk for approving a user
export const approveUser = createAsyncThunk(
  'admin/approveUser',
  async (userId, { rejectWithValue }) => {
    try {
      const response = await axiosInstance.patch(`/admin/users/${userId}`, { is_approved: true });
      return response.data; // The updated user object
    } catch (error) {
      Swal.fire('Approval Failed', error.response?.data?.message || 'Could not approve the user.', 'error');
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  users: [],
  isLoading: false,
  error: null,
};

const adminSlice = createSlice({
  name: 'admin',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchAllUsers.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchAllUsers.fulfilled, (state, action) => {
        state.isLoading = false;
        state.users = action.payload;
      })
      .addCase(fetchAllUsers.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(approveUser.fulfilled, (state, action) => {
        // Find and update the user in the state
        const index = state.users.findIndex(user => user.id === action.payload.id);
        if (index !== -1) {
          state.users[index] = action.payload;
        }
      });
  },
});

export default adminSlice.reducer;