from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
from app import views

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
app.secret_key = """d\xc8\xfb:)~\x1c\x04\x8c\x87\x84Dxm\xa5\\\x94\xea\xc4wY4\xdc\xf2"""
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)