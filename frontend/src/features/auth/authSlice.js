import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../api/axiosInstance';
import Swal from 'sweetalert2';

// Async thunk for user login
export const loginUser = createAsyncThunk(
  'auth/loginUser',
  async (credentials, { rejectWithValue }) => {
    try {
      const response = await axiosInstance.post('/auth/login', credentials);
      localStorage.setItem('token', response.data.access_token);
      // You would typically fetch user data here as well
      // For now, we'll just store the token
      return response.data;
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Login Failed',
        text: error.response?.data?.message || 'An unknown error occurred.',
      });
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  user: null,
  token: localStorage.getItem('token') || null,
  isLoading: false,
  isAuthenticated: !!localStorage.getItem('token'),
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      localStorage.removeItem('token');
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.token = action.payload.access_token;
        state.isAuthenticated = true;
        // In a real app, you would decode the token or fetch user data here
        // and set state.user
      })
      .addCase(loginUser.rejected, (state) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;