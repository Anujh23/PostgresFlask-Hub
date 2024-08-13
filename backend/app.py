from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS 
from os import environ

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    inventory_count = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'The server is running'})

# User routes
@app.route('/api/flask/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email}), 201
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': 'error creating user', 'error': str(e)}), 500)

@app.route('/api/flask/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(users_data), 200

@app.route('/api/flask/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200
    return make_response(jsonify({'message': 'user not found'}), 404)

@app.route('/api/flask/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    data = request.get_json()
    if user:
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        try:
            db.session.commit()
            return jsonify({'message': 'user updated'}), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'error updating user', 'error': str(e)}), 500)
    return make_response(jsonify({'message': 'user not found'}), 404)

@app.route('/api/flask/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'user deleted'}), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'error deleting user', 'error': str(e)}), 500)
    return make_response(jsonify({'message': 'user not found'}), 404)

# Product routes
@app.route('/api/flask/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'], inventory_count=data['inventory_count'])
    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'id': new_product.id, 'name': new_product.name, 'price': new_product.price, 'inventory_count': new_product.inventory_count}), 201
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': 'error creating product', 'error': str(e)}), 500)

@app.route('/api/flask/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_data = [{'id': product.id, 'name': product.name, 'price': product.price, 'inventory_count': product.inventory_count} for product in products]
    return jsonify(products_data), 200

@app.route('/api/flask/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'inventory_count': product.inventory_count}), 200
    return make_response(jsonify({'message': 'product not found'}), 404)

@app.route('/api/flask/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    data = request.get_json()
    if product:
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.inventory_count = data.get('inventory_count', product.inventory_count)
        try:
            db.session.commit()
            return jsonify({'message': 'product updated'}), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'error updating product', 'error': str(e)}), 500)
    return make_response(jsonify({'message': 'product not found'}), 404)

@app.route('/api/flask/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        try:
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'product deleted'}), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'error deleting product', 'error': str(e)}), 500)
    return make_response(jsonify({'message': 'product not found'}), 404)

# Order routes
@app.route('/api/flask/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(user_id=data['user_id'], total_price=data['total_price'])
    try:
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'id': new_order.id, 'user_id': new_order.user_id, 'total_price': new_order.total_price}), 201
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': 'error creating order', 'error': str(e)}), 500)

@app.route('/api/flask/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    orders_data = [{'id': order.id, 'user_id': order.user_id, 'total_price': order.total_price} for order in orders]
    return jsonify(orders_data), 200

@app.route('/api/flask/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if order:
        return jsonify({'id': order.id, 'user_id': order.user_id, 'total_price': order.total_price}), 200
    return make_response(jsonify({'message': 'order not found'}), 404)

@app.route('/api/flask/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)
    data = request.get_json()
    if order:
        order.user_id = data.get('user_id', order.user_id)
        order.total_price = data.get('total_price', order.total_price)
        try:
            db.session.commit()
            return jsonify({'message': 'order updated'}), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'error updating order', 'error': str(e)}), 500)
    return make_response(jsonify({'message': 'order not found'}), 404)

@app.route('/api/flask/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if order:
        try:
            db.session.delete(order)
            db.session.commit()
            return jsonify({'message': 'order deleted'}), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'error deleting order', 'error': str(e)}), 500)
    return make_response(jsonify({'message': 'order not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
