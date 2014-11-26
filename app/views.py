from app import app
from flask import render_template


@app.route("/", methods=["GET"])
def home():
    title = "Cooking challenge"
    return render_template('index-template.html', title=title)