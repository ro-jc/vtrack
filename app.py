from flask import (
    Flask, flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash

import db


app = Flask(__name__)
db.init_app(app)


@app.route("/")
def landing():
    return render_template('index.html', name=None)


@app.route("/signup", methods=('GET','POST'))
def signup():
    if request.method == 'POST':
        name = request.form['name']
        female = (request.form['gender'].lower() == 'female')
        phone_no = request.form['phoneNo']
        vit_mail = request.form['vitMail']
        password = request.form['password']
        
        database = db.get_db()
        crs = database.cursor(dictionary=True)
        error = None
        '''
        if x is None:
            error = 'blah blah blah'
        flash(error)
        '''
        if error is None:
            crs.execute(
                "INSERT INTO user (email, password, name, female, phone_number) "
                f"VALUES ('{vit_mail}', '{generate_password_hash(password)}', '{name}', {female}, '{phone_no}')"
            )
            database.commit()

        crs.execute("SELECT * FROM user ORDER BY userid DESC LIMIT 1")
        record = crs.fetchone()
        #else condition in case there was a new record added before this one could be read off the database
        # record['password'] = password if check_password_hash(record['password'], password) else "intermediate write"

    return render_template('signup.html', name=None)


@app.route("/login", methods=('GET','POST'))
def login():
    return render_template('login.html', name=None)


@app.route("/cabshare")
def cab_share():
    pass