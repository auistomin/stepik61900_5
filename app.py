from flask import Flask

from config import Config
from models import db, migrate

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.app_context().push()
migrate.init_app(app, db)

from views import *
from admin import admin

if __name__ == '__main__':
    app.run()