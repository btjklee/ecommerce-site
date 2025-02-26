import React from "react";
import { Link } from "react-router-dom";

const Cart = ({ cart }) => {
    return (
        <div className="container">
            <h2 className="text-center my-4">Shopping Cart</h2>
            {cart.length === 0 ? (
                <p className="text-center">Your cart is empty.</p>
            ) : (
                <table className="table table-bordered">
                    <thead className="table-dark">
                        <tr>
                            <th>Product</th>
                            <th>Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {cart.map((item, index) => (
                            <tr key={index}>
                                <td>{item.name}</td>
                                <td>${item.price.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
            <div className="text-center">
                <Link to="/checkout" className="btn btn-success">Proceed to Checkout</Link>
            </div>
        </div>
    );
};

export default Cart;
