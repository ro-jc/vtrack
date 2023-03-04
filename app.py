from flask import (
    Flask, flash, g, redirect, render_template, request, url_for
)
import db


app = Flask(__name__)
db.init_app(app)


@app.route("/")
def landing():
    return render_template('index.html', name=None)


@app.route("/signup", methods=('GET','POST'))
def signup():
    return render_template('signup.html', name=None)


@app.route("/login", methods=('GET','POST'))
def login():
    return render_template('login.html', name=None)


@app.route("/cabshare")
def cab_share():
    pass