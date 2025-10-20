import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUserDetails } from './features/auth/authSlice';
import AppRoutes from './routes/AppRoutes';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

function App() {
  const dispatch = useDispatch();
  // We get the user object from the state. It will initially have just the ID if a token is in localStorage.
  const { user, isAuthenticated } = useSelector((state) => state.auth);

  useEffect(() => {
    // This effect runs when the app loads
    // If the user is marked as authenticated but we don't have their full details (like a role),
    // it means they are a returning user. We need to fetch their data.
    if (isAuthenticated && user && !user.role) {
      dispatch(fetchUserDetails(user.id));
    }
  }, [isAuthenticated, user, dispatch]); // Dependencies for the effect

  return (
    <div className="App">
      <Navbar />
      <main className="main-content">
        <AppRoutes />
      </main>
      <Footer />
    </div>
  );
}

export default App;