from datetime import datetime as dt
from numpy import random

from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from forms import CheckoutForm, LoginForm, RegisterForm
from models import User, OrderMeals, Order, Meal, Category
from config import months
from app import app, db


# ================================================================================
# формат даты для заказа
@app.template_filter('date_format')
def date_format(date):
    day = dt.strftime(date, '%d').lstrip('0')
    month = months[int(dt.strftime(date, '%m')) - 1]
    return day + ' ' + month


# ================================================================================
# представление пользователя по его id
@app.template_filter('user_email')
def user_email(user_id):
    user = User.query.filter(User.id == user_id).first()
    return user.email


# ================================================================================
# это админ
@app.template_filter('is_admin')
def is_admin(user_id):
    return user_id == 1


# ================================================================================
# представление количества блюд
@app.template_filter('str_meals')
def str_meals(n):
    return 'блюд' + ('' if n % 10 == 0 or 4 < n % 10 < 10 or 10 < n % 100 < 15 else 'а' if 1 < n % 10 < 5 else 'о')


# ================================================================================
# итоговое количество в корзине
@app.context_processor
def cart_quantity():
    cart = session.get('cart', {})
    if not cart:
        res = 0
    else:
        res = sum([int(value['quantity']) for value in cart.values()])
    return dict(cart_quantity=res)


# ================================================================================
# итоговая сумма в корзине
@app.context_processor
def cart_sum():
    cart = session.get('cart', {})
    if not cart:
        res = 0
    else:
        res = sum([int(value['sum']) for value in cart.values()])
    return dict(cart_sum=res)


# ================================================================================
# главная страница
@app.route('/')
def render_index():

    categories = Category.query.all()
    meals = []
    for category in categories:
        catmeals = Meal.query.filter(Meal.category_id == category.id).all()
        random.shuffle(catmeals)
        meals += catmeals[0:3]

    return render_template('main.html', categories=categories, meals=meals)


# ================================================================================
# добавление товара в корзину
@app.route('/addtocart/<int:meal_id>/')
def render_addtocart(meal_id):

    meal = Meal.query.get_or_404(meal_id)
    meal_id = str(meal_id)
    cart = session.get('cart', {})
    if not meal_id in cart:
        cart[meal_id] = {'title': meal.title, 'quantity': 0, 'sum': 0}
    cart[meal_id]['quantity'] += 1
    cart[meal_id]['sum'] = cart[meal_id]['quantity'] * meal.price
    session['cart'] = cart

    return redirect('/cart/')


# ================================================================================
# корзина
@app.route('/cart/', methods=['GET', 'POST'])
def render_cart():

    form = CheckoutForm()
    sum = cart_sum()['cart_sum']
    cart = session.get('cart', {})
    is_auth = session.get('is_auth', False)

    if request.method == 'POST':
        if not is_auth:
            return redirect('/auth/')
        if form.validate_on_submit() and sum != 0:
            user_id = session.get('user_id', False)
            if not user_id:
                return redirect('/auth/')
            name = form.name.data
            address = form.address.data
            email = form.email.data
            phone = form.phone.data

            order = Order(date=dt.now(), sum=sum, status='Заказ принят', email=email, phone=phone, address=address, user_id=user_id)
            for key, value in cart.items():
                meal = Meal.query.filter(Meal.id == key).first()
                stock = OrderMeals(order_id=order.id, meal_id=meal.id, quantity=value['quantity'], sum=value['sum'])
                order.stock.append(stock)
                meal.stock.append(stock)
                db.session.add(stock)
            db.session.add(order)
            db.session.commit()

            session.pop('cart')
            return render_template('ordered.html')

    return render_template('cart.html', form=form)


# ================================================================================
# удаление товара из корзины
@app.route('/cart/delete/<int:meal_id>/')
def render_cart_delete(meal_id):

    form = CheckoutForm()

    meal = Meal.query.get_or_404(meal_id)
    meal_id = str(meal_id)
    cart = session.get('cart', {})
    if meal_id in cart:
        cart.pop(meal_id)
    if cart:
        session['cart'] = cart
    else:
        session.pop('cart')

    return render_template('cart.html', form=form)


# ================================================================================
# подтверждение заказа
@app.route('/ordered/')
def render_ordered():
    return render_template('ordered.html')


# ================================================================================
# аутентификация
@app.route('/auth/', methods=['GET', 'POST'])
def render_auth():

    is_auth = session.get('is_auth', False)
    if is_auth:
        return redirect('/account/')

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter(User.email == email).first()
            if not user:
                form.email.errors.append('Пользователь не найден')
            elif not check_password_hash(user.password, password):
                form.password.errors.append('Введен неверный пароль')
            else:
                session['is_auth'] = True
                session['user_id'] = user.id
                return redirect('/account/')

    return render_template('auth.html', form=form)


# ================================================================================
# регистрация
@app.route('/register/', methods=['GET', 'POST'])
def render_register():

    is_auth = session.get('is_auth', False)
    if is_auth:
        return redirect('/account/')

    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter(User.email == email).first()
            if user:
                form.email.errors.append('Пользователь с таким e-mail уже есть в базе')
            else:
                user = User(email=email, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                session['is_auth'] = True
                session['user_id'] = user.id
                return redirect('/account/')

    return render_template('register.html', form=form)


# ================================================================================
# личный кабинет
@app.route('/account/')
def render_account():

    is_auth = session.get('is_auth', False)
    if not is_auth:
        return redirect('/auth/')

    orders = Order.query.filter(Order.user_id == session['user_id']).order_by(Order.date.desc())
    meals = {}
    for order in orders:
        for item in order.stock:
            if not item.meal_id in meals:
                meal = Meal.query.filter(Meal.id == item.meal_id).first()
                meals[item.meal_id] = meal.title
    return render_template('account.html', orders=orders, meals=meals)


# ================================================================================
# выход из аккаунта
@app.route('/logout/')
def logout_route():
    session.clear()
    return redirect('/auth/')


# ================================================================================
# страница при ошибке 404
@app.errorhandler(404)
def render_404(error):
    return render_template('404.html')