import React, { useEffect, useState } from 'react';
import "../assets/style.css";  // or wherever your inventory styles live

const Inventory = () => {
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/inventory')  // This assumes your Express route is live
      .then(res => res.json())
      .then(data => {
        setCars(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch inventory:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading inventory...</p>;

  return (
    <div className="inventory-list">
      <h2>Available Cars</h2>
      {cars.length === 0 ? (
        <p>No cars available at the moment.</p>
      ) : (
        cars.map(car => (
          <div key={`${car.dealer_id}-${car.model}`} className="car-card">
            <h3>{car.make} {car.model}</h3>
            <p>Type: {car.bodyType}</p>
            <p>Year: {car.year} | Mileage: {car.mileage} km</p>
            <p>Dealer ID: {car.dealer_id}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default Inventory;
