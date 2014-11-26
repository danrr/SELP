from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/", methods=["GET"])
def home():
    return "hello"

if __name__ == "__main__":
    app.run()

