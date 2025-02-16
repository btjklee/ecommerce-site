import React, { useState } from "react";

const Checkout = ({ cart }) => {
    const [name, setName] = useState("");
    const [address, setAddress] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const orderData = {
            name,
            address,
            items: cart,  // Send cart items
        };

        try {
            const response = await fetch("http://localhost:5000/checkout", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(orderData),
            });

            if (response.ok) {
                alert("Order submitted successfully!");
                // Optionally clear cart here
            } else {
                alert("Order submission failed.");
            }
        } catch (error) {
            console.error("Error submitting order:", error);
        }
    };

    return (
        <div>
            <h2>Checkout</h2>
            <form onSubmit={handleSubmit}>
                <label>Name: <input type="text" value={name} onChange={(e) => setName(e.target.value)} required /></label>
                <br />
                <label>Address: <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} required /></label>
                <br />
                <button type="submit">Submit Order</button>
            </form>
        </div>
    );
};

export default Checkout;
