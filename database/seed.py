from csv import DictReader
from os import path, remove as remove_file

from werkzeug.security import generate_password_hash

from app import db
from models import User, Meal, Category


def seed():

    # категории
    with open('delivery_categories.csv', 'r', encoding="utf-8") as file:
        reader = DictReader(file, delimiter=',')
        for line in reader:
            category = Category(
                id=line['id'],
                title=line['title']
            )
            db.session.add(category)
            db.session.flush()

    # блюда
    with open('delivery_items.csv', 'r', encoding="utf-8") as file:
        reader = DictReader(file, delimiter=',')
        for line in reader:
            meal = Meal(
                id=line['id'],
                title=line['title'],
                price=line['price'],
                description=line['description'],
                picture=line['picture'],
                category_id=line['category_id']
            )
            db.session.add(meal)
    db.session.commit()

    # пользователь админ
    user = User(email='admin@app.py', password=generate_password_hash('admin'))
    db.session.add(user)
    db.session.commit()

    '''
    # тест создания связей в таблице OrderMeals
    from datetime import datetime as dt
    from models import OrderMeals, Order
    order = Order(date=dt.now(), sum=555.55, status='Заказ принят', email='qwe@qwe.qwe', phone='87776665544', address='qwe123', user_id=user.id)
    meal1 = Meal.query.filter(Meal.id == 1).first()
    meal2 = Meal.query.filter(Meal.id == 2).first()
    stock1 = OrderMeals(order_id=order.id, meal_id=meal1.id, quantity=20, sum=222.22)
    stock2 = OrderMeals(order_id=order.id, meal_id=meal2.id, quantity=30, sum=333.33)
    order.stock.append(stock1)
    order.stock.append(stock2)
    meal1.stock.append(stock1)
    meal2.stock.append(stock2)
    db.session.add(order)
    db.session.add(stock1)
    db.session.add(stock2)
    db.session.commit()
    '''


def main():
    filename = path.dirname(path.realpath(__file__)) + '\\base.db'
    if path.exists(filename):
        remove_file(filename)
    db.create_all()
    seed()


# перед запуском в app.py отключить роуты (и формы),
# т.к. они ссылаются на несуществующую пока базу данных
if __name__ == '__main__':
    main()