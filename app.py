from flask import (
    Flask, flash, g, redirect, render_template, request, url_for
)

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template('index.html', name=None)