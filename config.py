from os import environ, path

months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


DATABASE_URL = environ.get('DATABASE_URL')
if DATABASE_URL is None:
    current_path = path.dirname(path.realpath(__file__))
    DATABASE_URL = 'sqlite:///' + current_path + '\\database\\base.db'


class Config:
    DEBUG = True
    SECRET_KEY = '13e0243b736a7cc203a040cee63cadeb'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False