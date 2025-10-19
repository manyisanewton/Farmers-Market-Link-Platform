// src/pages/RegisterPage.test.js
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import RegisterPage from '../pages/RegisterPage';
import { store } from '../app/store';
import axiosInstance from '../api/axiosInstance';
import Swal from 'sweetalert2';

// Mock the entire axiosInstance to control API calls in tests
jest.mock('../api/axiosInstance');

// Mock sweetalert2
jest.mock('sweetalert2', () => ({
  fire: jest.fn(),
}));

describe('RegisterPage', () => {
  beforeEach(() => {
    // Clear mock history before each test
    axiosInstance.post.mockClear();
    Swal.fire.mockClear();
  });

  const renderComponent = () =>
    render(
      <Provider store={store}>
        <BrowserRouter>
          <RegisterPage />
        </BrowserRouter>
      </Provider>
    );

  test('renders registration form correctly', () => {
    renderComponent();
    expect(screen.getByRole('heading', { name: /create an account/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/phone number/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/register as a/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /register/i })).toBeInTheDocument();
  });

  test('allows user input in all fields', () => {
    renderComponent();
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'johndoe' } });
    fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'john@example.com' } });
    fireEvent.change(screen.getByLabelText(/phone number/i), { target: { value: '+254712345678' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.change(screen.getByLabelText(/register as a/i), { target: { value: 'farmer' } });

    expect(screen.getByLabelText(/username/i).value).toBe('johndoe');
    expect(screen.getByLabelText(/email address/i).value).toBe('john@example.com');
    expect(screen.getByLabelText(/phone number/i).value).toBe('+254712345678');
    expect(screen.getByLabelText(/password/i).value).toBe('password123');
    expect(screen.getByLabelText(/register as a/i).value).toBe('farmer');
  });

  test('calls axios.post on form submission with correct data', async () => {
    // Mock a successful API response
    axiosInstance.post.mockResolvedValue({
      status: 201,
      data: { message: 'User created successfully' },
    });

    renderComponent();

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'johndoe' } });
    fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'john@example.com' } });
    fireEvent.change(screen.getByLabelText(/phone number/i), { target: { value: '+254712345678' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.change(screen.getByLabelText(/register as a/i), { target: { value: 'farmer' } });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    // Wait for the async submission to complete
    await waitFor(() => {
      expect(axiosInstance.post).toHaveBeenCalledTimes(1);
      expect(axiosInstance.post).toHaveBeenCalledWith('/auth/register', {
        username: 'johndoe',
        email: 'john@example.com',
        phone_number: '+254712345678',
        password: 'password123',
        role: 'farmer',
      });
    });
  });

  test('shows a success message and navigates on successful registration', async () => {
    axiosInstance.post.mockResolvedValue({
      status: 201,
      data: { message: 'User created successfully' },
    });

    renderComponent();

    // Fill and submit form
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'janedoe' } });
    fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'jane@example.com' } });
    fireEvent.change(screen.getByLabelText(/phone number/i), { target: { value: '+254787654321' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.change(screen.getByLabelText(/register as a/i), { target: { value: 'buyer' } });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    // Check for success alert
    await waitFor(() => {
      expect(Swal.fire).toHaveBeenCalledWith(expect.objectContaining({
        icon: 'success',
        title: 'Registration Successful!',
      }));
    });
  });
});