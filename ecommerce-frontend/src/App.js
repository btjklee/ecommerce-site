import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Cart from './Cart';
import Checkout from './Checkout';
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
    const [products, setProducts] = useState([]);
    const [cart, setCart] = useState([]);

    useEffect(() => {
        fetch('https://ecommerce-site-l9ti.onrender.com/products')
            .then(response => response.json())
            .then(data => setProducts(data))
            .catch(error => console.error("Error fetching products:", error));
    }, []);

    const addToCart = (product) => {
        setCart([...cart, product]);
    };

    return (
        <Router>
            {/* Navbar */}
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                <div className="container">
                    <Link className="navbar-brand" to="/">E-Shop</Link>
                    <div className="collapse navbar-collapse">
                        <ul className="navbar-nav ms-auto">
                            <li className="nav-item">
                                <Link className="nav-link" to="/">Home</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/cart">Cart ({cart.length})</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/checkout">Checkout</Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>

            {/* Routes */}
            <div className="container mt-4">
                <Routes>
                    <Route path="/" element={
                        <div>
                            <h1 className="text-center">Welcome to E-Shop</h1>
                            <div className="row">
                                {products.map(product => (
                                    <div className="col-md-4 mb-4" key={product.id}>
                                        <div className="card shadow-sm">
                                            <img src="https://via.placeholder.com/150" className="card-img-top" alt="Product" />
                                            <div className="card-body text-center">
                                                <h5 className="card-title">{product.name}</h5>
                                                <p className="card-text">${product.price.toFixed(2)}</p>
                                                <button className="btn btn-primary" onClick={() => addToCart(product)}>Add to Cart</button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    } />
                    <Route path="/cart" element={<Cart cart={cart} />} />
                    <Route path="/checkout" element={<Checkout cart={cart} />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;

