import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import stripe

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)

class Order(db.Model):
    __tablename__ = 'orders'  # Fix SQL conflict

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.Column(db.Text, nullable=False)  # JSON stored as text

def populate_default_products():
    """Ensure default products exist in the database after a restart."""
    if not Product.query.first():  # Check if products table is empty
        print("No products found. Adding default products...")
        default_products = [
            {"name": "Laptop", "price": 999.99, "description": "A powerful laptop",
             "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8"},
            {"name": "Smartphone", "price": 799.99, "description": "Latest model smartphone",
             "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9"},
            {"name": "Headphones", "price": 199.99, "description": "Noise-canceling headphones",
             "image": "https://images.unsplash.com/photo-1516387938699-a93567ec168e"},
            {"name": "Smartwatch", "price": 249.99, "description": "Water-resistant smartwatch",
             "image": "https://images.unsplash.com/photo-1600096194903-3d5debb81d36"},
            {"name": "Gaming Mouse", "price": 89.99, "description": "RGB gaming mouse",
             "image": "https://images.unsplash.com/photo-1606821851227-0cb2f4b0a95a"}
        ]

        for product in default_products:
            new_product = Product(**product)
            db.session.add(new_product)
        
        db.session.commit()
        print("Default products added.")

# Initialize database and populate products if missing
with app.app_context():
    print("Creating database tables if they don't exist...")
    db.create_all()
    populate_default_products()

@app.route('/')
def home():
    return "E-commerce Backend is Running!"

### ---- PRODUCT ROUTES ---- ###
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price, "description": p.description, "image": p.image}
        for p in products
    ])

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_product = Product(
        name=data['name'],
        price=data['price'],
        description=data.get('description', ''),
        image=data.get('image', '')  # Ensure image field is included
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201

@app.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found!"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"})

### ---- CHECKOUT & ORDER ROUTES ---- ###
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

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([
        {"id": o.id, "name": o.name, "address": o.address, "items": json.loads(o.items)}
        for o in orders
    ])

# Stripe Integration
stripe.api_key = "sk_test_51Qtawu2NvkwdcPoHb8CzLo3nDobOA64KQ1ZZDpe084Jbk239Pv9auOD7A9emwrcFnuN3ADtEKzci9dCQx56GPKTq00cnNvUfhP"

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = request.json
        amount = int(data['amount'] * 100)  # Stripe uses cents
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd'
        )
        return jsonify({'clientSecret': intent['client_secret']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default port 5000
    app.run(host='0.0.0.0', port=port, debug=False)
