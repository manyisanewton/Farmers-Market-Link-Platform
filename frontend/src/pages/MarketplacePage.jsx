// src/pages/MarketplacePage.jsx
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchProduce } from '../features/produce/produceSlice';
import ProduceCard from '../components/specific/ProduceCard';
import './MarketplacePage.css';

const MarketplacePage = () => {
  const dispatch = useDispatch();
  
  // --- THIS IS THE FIX ---
  // 1. Select the entire 'produce' slice.
  // 2. Provide a default empty object {} to prevent the destructuring error on initial render.
  const { items: produceItems, isLoading } = useSelector((state) => state.produce) || {};

  const [filters, setFilters] = useState({ name: '', location: '', min_price: '', max_price: '' });

  useEffect(() => {
    dispatch(fetchProduce());
  }, [dispatch]);

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleFilterSubmit = (e) => {
    e.preventDefault();
    dispatch(fetchProduce(filters));
  };

  return (
    <div className="marketplace-container">
      <header className="marketplace-header">
        <h1>Marketplace</h1>
        <p>Browse fresh produce directly from local farmers.</p>
      </header>

      <aside className="filter-sidebar">
        <h3>Filter Produce</h3>
        <form onSubmit={handleFilterSubmit}>
          <input type="text" name="name" placeholder="Crop Name (e.g., Tomatoes)" value={filters.name} onChange={handleFilterChange} />
          <input type="text" name="location" placeholder="Location (e.g., Nakuru)" value={filters.location} onChange={handleFilterChange} />
          <input type="number" name="min_price" placeholder="Min Price (KES)" value={filters.min_price} onChange={handleFilterChange} />
          <input type="number" name="max_price" placeholder="Max Price (KES)" value={filters.max_price} onChange={handleFilterChange} />
          <button type="submit">Apply Filters</button>
        </form>
      </aside>

      <main className="produce-grid-container">
        {isLoading ? (
          <p>Loading produce...</p>
        ) : produceItems && produceItems.length > 0 ? ( // Also check if produceItems exists before checking length
          <div className="produce-grid">
            {produceItems.map((produce) => (
              <ProduceCard key={produce.id} produce={produce} />
            ))}
          </div>
        ) : (
          <p>No produce found matching your criteria.</p>
        )}
      </main>
    </div>
  );
};

export default MarketplacePage;