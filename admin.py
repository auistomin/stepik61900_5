from flask import redirect, request, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app import app, db
from models import User, Order, Meal, Category


admin = Admin(app)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Order, db.session))


@app.before_request
def render_admin():
    if 'admin' in request.url:
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/auth/')
        elif int(user_id) != 1:
            return redirect('/account/')