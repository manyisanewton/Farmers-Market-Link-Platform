import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import AddProduce from '../pages/FarmerDashboard/AddProduce';
import { store } from '../app/store';
import axiosInstance from '../api/axiosInstance';
import Swal from 'sweetalert2';

// Mock axios and sweetalert2
jest.mock('../api/axiosInstance');
jest.mock('sweetalert2', () => ({
  fire: jest.fn(),
}));

describe('AddProduce Form', () => {
  beforeEach(() => {
    axiosInstance.post.mockClear();
    Swal.fire.mockClear();
  });

  const renderComponent = () =>
    render(
      <Provider store={store}>
        <BrowserRouter>
          <AddProduce />
        </BrowserRouter>
      </Provider>
    );

  test('renders the Add Produce form correctly', () => {
    renderComponent();
    expect(screen.getByRole('heading', { name: /add new produce/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/produce name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/price/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/quantity/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/unit/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/location/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/produce image/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /add produce/i })).toBeInTheDocument();
  });

  test('calls axios.post with form data on submission', async () => {
    axiosInstance.post.mockResolvedValue({ status: 201 }); // Mock successful submission

    renderComponent();

    // Fill the form
    fireEvent.change(screen.getByLabelText(/produce name/i), { target: { value: 'Fresh Carrots' } });
    fireEvent.change(screen.getByLabelText(/price/i), { target: { value: '50' } });
    fireEvent.change(screen.getByLabelText(/quantity/i), { target: { value: '100' } });
    fireEvent.change(screen.getByLabelText(/unit/i), { target: { value: 'bunch' } });
    fireEvent.change(screen.getByLabelText(/location/i), { target: { value: 'Kisumu' } });
    
    // Fake file upload
    const fakeFile = new File(['(⌐□_□)'], 'photo.png', { type: 'image/png' });
    fireEvent.change(screen.getByLabelText(/produce image/i), { target: { files: [fakeFile] } });

    // Submit
    fireEvent.click(screen.getByRole('button', { name: /add produce/i }));

    await waitFor(() => {
      expect(axiosInstance.post).toHaveBeenCalledTimes(1);
      
      // Axios with multipart/form-data uses a FormData object.
      // We check if it was called with an instance of FormData.
      expect(axiosInstance.post).toHaveBeenCalledWith(
        '/produce/',
        expect.any(FormData), // The payload is FormData
        expect.any(Object) // The third argument is the config with headers
      );
    });
  });
});