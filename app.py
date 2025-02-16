import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.Column(db.Text, nullable=False)  # JSON stored as text

# Create database tables on startup
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "E-commerce Backend is Running!"

### ---- PRODUCT ROUTES ---- ###

# Get All Products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price, "description": p.description}
        for p in products
    ])

# Add a Product
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_product = Product(
        name=data['name'],
        price=data['price'],
        description=data.get('description', '')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201

# Delete a Product
@app.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found!"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"})

### ---- CHECKOUT & ORDER ROUTES ---- ###

# Handle Checkout & Save Orders in Database
@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    if not data or 'name' not in data or 'address' not in data or 'items' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_order = Order(
        name=data['name'],
        address=data['address'],
        items=json.dumps(data['items'])  # Store as JSON string
    )
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({"message": "Order placed successfully!"}), 201

# Get All Orders (For Admin)
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([
        {"id": o.id, "name": o.name, "address": o.address, "items": json.loads(o.items)}
        for o in orders
    ])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default port 5000
    app.run(host='0.0.0.0', port=port, debug=True)
