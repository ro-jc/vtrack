from flask import (
    Flask, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta

import db


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=open('secret.txt').read()
)
db.init_app(app)


@app.route("/")
def landing():
    return render_template('index.html',
                           signed_in=bool(session.get('userid', None)))


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
def cab_share():
    if request.method == 'POST':
        print(request.form)
        pickup_point = request.form['from']
        drop_point = request.form['to']

        date_time = datetime.strptime(
            f"{request.form['date']} {request.form['time']}", '%Y:%m:%d %H:%M')

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
                    f"gender_filter={gender_filter} AND "
                    "resolved!=TRUE AND "
                    f"pickup_point={pickup_point} AND "
                    f"drop_point={drop_point} AND "
                    f"date={date_time.strftime('%Y:%m:%d')} AND "
                    f"vehicle={vehicle_type}")

        records = crs.fetchall()
        for record in records:
            record['datetime'] = datetime.strptime(
                f"{record['date']} {record['time']}", '%Y:%m:%d %H:%M:%S')
        records.sort(key=lambda record: abs(record['datetime']-date_time))

        return render_template('cabShareList.html', records=records, female=female)

    female = session['userid'][0] == 'F'
    return render_template('cabShareSearch.html', female=female)
