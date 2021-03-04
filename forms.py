from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Length, Email, Regexp, EqualTo
from wtforms.fields.html5 import TelField


# ================================================================================
# формирование заказа
class CheckoutForm(FlaskForm):
    name = StringField('Ваше имя', validators=[InputRequired('Введите имя'),
                                               Length(min=2, max=100, message='Имя должно быть не менее 2 символов и не более 100 символов')])
    address = StringField('Адрес', validators=[InputRequired('Введите адрес'),
                                               Length(min=5, message='Адрес не должен быть менее 5 символов')])
    email = StringField('Электропочта', validators=[InputRequired('Введите электронную почту'),
                                                    Email(message='Адрес электронной почты имеет некорректный формат')])
    phone = TelField('Телефон', validators=[InputRequired('Введите номер телефона'),
                                            Regexp('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', message='Номер телефона имеет некорректный формат')])
    submit = SubmitField('Оформить заказ')


# ================================================================================
# аутентификация
class LoginForm(FlaskForm):
    email = StringField('Электропочта', validators=[InputRequired('Введите электронную почту'),
                                                    Email(message='Адрес электронной почты имеет некорректный формат')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


# ================================================================================
# регистрация
class RegisterForm(FlaskForm):
    email = StringField('Электропочта', validators=[InputRequired('Введите электронную почту'),
                                                    Email(message='Адрес электронной почты имеет некорректный формат')])
    password = PasswordField('Пароль', validators=[DataRequired(),
                                                   Length(min=5, message='Пароль не должен быть менее 5 символов')])
    submit = SubmitField('Зарегистрироваться')