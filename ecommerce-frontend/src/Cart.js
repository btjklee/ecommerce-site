import React from 'react';
import { Link } from 'react-router-dom';

const Cart = ({ cart }) => {
    return (
        <div>
            <h2>Shopping Cart</h2>
            <ul>
                {cart.map((item, index) => (
                    <li key={index}>{item.name} - ${item.price.toFixed(2)}</li>
                ))}
            </ul>
            {cart.length > 0 && (
                <Link to="/checkout">
                    <button>Proceed to Checkout</button>
                </Link>
            )}
        </div>
    );
};

export default Cart;
