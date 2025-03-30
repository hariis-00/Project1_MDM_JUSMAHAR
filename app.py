from flask import Flask
from flask.helpers import send_file
app = Flask(__name__)
@app.route("/")
def indexPage():
    return send_file("frontend/index.html")