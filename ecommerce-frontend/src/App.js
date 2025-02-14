import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
    const [products, setProducts] = useState([]);

    useEffect(() => {
      axios.get("http://127.0.0.1:10000/products")      // Flask API endpoint
            .then(response => setProducts(response.data))
            .catch(error => console.error("Error fetching data:", error));
    }, []);

    return (
        <div>
            <h1>Welcome to My E-commerce Site</h1>
            <h2>Products</h2>
            <ul>
                {products.map(product => (
                    <li key={product.id}>{product.name} - ${product.price}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;
