import React, { useState } from "react";
import { loadStripe } from "@stripe/stripe-js";
import { Elements, CardElement, useStripe, useElements } from "@stripe/react-stripe-js";

const stripePromise = loadStripe("pk_test_YOUR_PUBLISHABLE_KEY");

const CheckoutForm = ({ totalAmount }) => {
    const stripe = useStripe();
    const elements = useElements();
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const { paymentMethod, error } = await stripe.createPaymentMethod({
            type: "card",
            card: elements.getElement(CardElement),
        });

        if (error) {
            setError(error.message);
            return;
        }

        const response = await fetch("https://ecommerce-site-l9ti.onrender.com/create-payment-intent", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ amount: totalAmount }),
        });

        const { clientSecret } = await response.json();
        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: paymentMethod.id,
        });

        if (result.error) {
            setError(result.error.message);
        } else {
            alert("Payment Successful!");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <CardElement />
            {error && <p style={{ color: "red" }}>{error}</p>}
            <button type="submit" disabled={!stripe}>Pay Now</button>
        </form>
    );
};

const Checkout = ({ cart }) => {
    const totalAmount = cart.reduce((sum, item) => sum + item.price, 0);

    return (
        <Elements stripe={stripePromise}>
            <h2>Checkout</h2>
            <CheckoutForm totalAmount={totalAmount} />
        </Elements>
    );
};

export default Checkout;

