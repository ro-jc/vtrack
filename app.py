from flask import (
    Flask, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
import functools

from datetime import datetime, timedelta

import db


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=open('secret.txt').read()
)
db.init_app(app)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('userid', None):
            return redirect(url_for('landing'))
        return view(**kwargs)
    return wrapped_view


def is_female():
    return session['userid'][0] == 'F'


@app.route("/")
def landing():
    if session.get('userid', None):
        return render_template('landing.html')
    else:
        return render_template('index.html')


@app.route("/signup", methods=('GET', 'POST'))
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
        # add else condition in case there was a new record added before this one could be read off the database
        session['userid'] = ('F' if record['female'] ==
                             'true' else 'M') + str(record['userid'])

        return redirect(url_for('landing'))
    
    

    return render_template('signup.html')


@app.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
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
                f"SELECT userid,password,female FROM user where email='{vit_mail}'")

        record = crs.fetchone()
        print(record['password'])
        print()
        if check_password_hash(record['password'], password):

            session['userid'] = ('F' if record['female'] ==
                                 'true' else 'M') + str(record['userid'])
            return redirect(url_for('landing'))
        else:
            flash('Wrong credentials')

    return render_template('login.html')


@app.route("/cabshare", methods=('GET', 'POST'))
@login_required
def cab_share():
    if request.method == 'POST':
        print(request.form)
        pickup_point = request.form['from']
        drop_point = request.form['to']
        date = request.form['date']
        if 'time' in request.form:
            date_time = datetime.strptime(
                f"{date} {request.form['time']}", '%Y-%m-%d %H:%M')

        gender_filter = (request.form.get('genderFilter', 'off') == 'on')

        vehicle_types = {
            'any': 0,
            'cab': 1,
            'auto': 2
        }
        vehicle_type = vehicle_types.get(request.form['vehicleType'], 0)

        database = db.get_db()
        crs = database.cursor(dictionary=True)
        crs.execute(f"SELECT * FROM trips WHERE "
                    "resolved!=TRUE AND "
                    f"gender_filter={gender_filter} AND "
                    f"pickup_point='{pickup_point}' AND "
                    f"drop_point='{drop_point}' AND "
                    f"vehicle={vehicle_type} AND "
                    f"trip_date='{date}'")

        records = crs.fetchall()
        for record in records:
            record['datetime'] = datetime.strptime(
                f"{record['date']} {record['time']}", '%Y-%m-%d %H:%M:%S')
        records.sort(key=lambda record: abs(record['datetime']-date_time))

        if 'time' in request.form:
            records.sort(key=lambda record: abs(record['datetime']-date_time))
        else:
            records.sort(key=lambda record: record['datetime'])

        return render_template('cabShareList.html', records=records, female=is_female())

    return render_template('cabShareSearch.html', female=is_female())
