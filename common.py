import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from config import Config
from flask_migrate import Migrate





app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


# debug = app.logger.debug
# info = app.logger.info
