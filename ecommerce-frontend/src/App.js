import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Cart from './Cart';
import Checkout from './Checkout';

const App = () => {
    const [products, setProducts] = useState([]);
    const [cart, setCart] = useState(() => {
        // Load cart from localStorage on initial render
        const savedCart = localStorage.getItem("cart");
        return savedCart ? JSON.parse(savedCart) : [];
    });

    // Fetch products from backend when page loads
    useEffect(() => {
        fetch('https://ecommerce-site-l9ti.onrender.com/products')
            .then(response => response.json())
            .then(data => setProducts(data))
            .catch(error => console.error("Error fetching products:", error));
    }, []);

    // Update localStorage whenever cart changes
    useEffect(() => {
        localStorage.setItem("cart", JSON.stringify(cart));
    }, [cart]);

    const addToCart = (product) => {
        setCart([...cart, product]);
    };

    return (
        <Router>
            <nav>
                <Link to="/">Home</Link> | <Link to="/cart">Cart ({cart.length})</Link>
            </nav>

            <Routes>
                <Route path="/" element={
                    <div>
                        <h1>Welcome to My E-Commerce Site</h1>
                        <h2>Products</h2>
                        <ul>
                            {products.map(product => (
                                <li key={product.id}>
                                    {product.name} - ${product.price.toFixed(2)}
                                    <button onClick={() => addToCart(product)}>Add to Cart</button>
                                </li>
                            ))}
                        </ul>
                    </div>
                } />
                <Route path="/cart" element={<Cart cart={cart} />} />
                <Route path="/checkout" element={<Checkout cart={cart} />} />
                <Route path="/thank-you" element={<h2>Thank you for your order!</h2>} />
            </Routes>
        </Router>
    );
};

export default App;
