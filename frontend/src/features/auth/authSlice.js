// src/features/auth/authSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../api/axiosInstance';
import Swal from 'sweetalert2';
import { jwtDecode } from 'jwt-decode';

// Helper function to get initial user state from localStorage
const getInitialState = () => {
  const token = localStorage.getItem('token');
  if (token) {
    try {
      const decoded = jwtDecode(token);
      // We only store the ID initially. The role is fetched on app load.
      return {
        token,
        isAuthenticated: true,
        user: { id: decoded.sub }, // Store user ID from token's 'sub' claim
        isLoading: false,
      };
    } catch (error) {
      localStorage.removeItem('token');
    }
  }
  // Default state if no token is found
  return {
    user: null,
    token: null,
    isLoading: false,
    isAuthenticated: false,
  };
};

// Async thunk for fetching full user details by ID
export const fetchUserDetails = createAsyncThunk(
  'auth/fetchUserDetails',
  async (userId, { rejectWithValue }) => {
    try {
      const response = await axiosInstance.get(`/users/${userId}`);
      return response.data; // Returns { id, username, email, role }
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Async thunk for user login
export const loginUser = createAsyncThunk(
  'auth/loginUser',
  async (credentials, { dispatch, rejectWithValue }) => {
    try {
      const response = await axiosInstance.post('/auth/login', credentials);
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      
      const decoded = jwtDecode(access_token);
      
      // Fetch user details and wait for the action to complete
      const userDetailsAction = await dispatch(fetchUserDetails(decoded.sub));

      // Check if fetching details failed
      if (fetchUserDetails.rejected.match(userDetailsAction)) {
        throw new Error('Failed to fetch user details after login.');
      }

      // Return a complete payload with the token AND the full user object
      return { access_token: access_token, user: userDetailsAction.payload };

    } catch (error) {
      localStorage.removeItem('token'); // Ensure cleanup on any failure
      Swal.fire({
        icon: 'error',
        title: 'Login Failed',
        text: error.response?.data?.message || 'An unknown error occurred.',
      });
      return rejectWithValue(error.response?.data);
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState: getInitialState(),
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
      // Cases for loginUser
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        // The payload from loginUser is now { access_token, user }
        state.isLoading = false;
        state.token = action.payload.access_token;
        state.user = action.payload.user; // Set the full user object in the state
        state.isAuthenticated = true;
      })
      .addCase(loginUser.rejected, (state) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
      })
      // Cases for fetchUserDetails (primarily for app load)
      .addCase(fetchUserDetails.fulfilled, (state, action) => {
        // This runs on initial app load if a token is present
        if (state.isAuthenticated) {
          state.user = action.payload;
        }
      })
      .addCase(fetchUserDetails.rejected, (state) => {
        // If fetching details for a returning user fails, log them out
        localStorage.removeItem('token');
        state.user = null;
        state.token = null;
        state.isAuthenticated = false;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;