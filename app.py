import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Create database tables when the app starts
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "E-commerce site is running!"

# Route to Add a Product
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_product = Product(name=data['name'], price=data['price'], description=data.get('description', ''))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201

# Route to Get All Products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "description": p.description} for p in products])

@app.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found!"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Default to 10000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)
