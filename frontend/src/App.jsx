// src/App.jsx
import React from 'react';
import AppRoutes from './routes/AppRoutes';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

function App() {
  return (
    <div className="App">
      <Navbar />
      <main>
        <AppRoutes />
      </main>
      <Footer />
    </div>
  );
}

export default App;