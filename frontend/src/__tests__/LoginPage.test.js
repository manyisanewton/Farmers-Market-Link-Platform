// src/pages/LoginPage.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import LoginPage from '../pages/LoginPage';
import { store } from '../app/store'; // Import the REAL store

// Mock the entire authSlice to control the dispatch
const mockDispatch = jest.fn();
jest.mock('react-redux', () => ({
  ...jest.requireActual('react-redux'),
  useDispatch: () => mockDispatch,
}));

// Mock sweetalert2
jest.mock('sweetalert2', () => ({
  fire: jest.fn(),
}));

describe('LoginPage', () => {
  beforeEach(() => {
    // Clear mock history before each test
    mockDispatch.mockClear();
  });

  // Use the real store for rendering, but mock the dispatch action
  const renderComponent = () =>
    render(
      <Provider store={store}>
        <BrowserRouter>
          <LoginPage />
        </BrowserRouter>
      </Provider>
    );

  test('renders login form correctly', () => {
    renderComponent();
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  test('allows user to type into email and password fields', () => {
    renderComponent();
    const emailInput = screen.getByLabelText(/email address/i);
    const passwordInput = screen.getByLabelText(/password/i);

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    expect(emailInput.value).toBe('test@example.com');
    expect(passwordInput.value).toBe('password123');
  });

  test('dispatches loginUser action on form submission', () => {
    renderComponent();

    fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // Check that our mocked dispatch was called.
    // The call will contain the async thunk action creator.
    expect(mockDispatch).toHaveBeenCalledTimes(1);
    // You can add more specific assertions here if needed, but this is the core test
  });
});