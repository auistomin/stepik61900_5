from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', back_populates='users')


class OrderMeals(db.Model):
    __tablename__ = 'order_meals'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    sum = db.Column(db.Float, nullable=False)
    meal = db.relationship("Meal", back_populates="stock")
    order = db.relationship("Order", back_populates="stock")


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', back_populates='orders')
    #meals = db.relationship('Meal', secondary=orders_meals, back_populates='orders')
    stock = db.relationship('OrderMeals', backref='orders', primaryjoin=id == OrderMeals.order_id)


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(), nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    categories = db.relationship('Category', back_populates='meals')
    #orders = db.relationship('Order', secondary=orders_meals, back_populates='meals')
    orders = db.relationship(OrderMeals, back_populates="meal")
    stock = db.relationship('OrderMeals', backref='meals', primaryjoin=id == OrderMeals.meal_id)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    meals = db.relationship('Meal', back_populates='categories')