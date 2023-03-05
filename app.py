from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import functools

from datetime import datetime
from pickle import load, dump


import db


app = Flask(__name__)
app.config.from_mapping(SECRET_KEY=open("secret.txt").read())
db.init_app(app)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("userid", None):
            return redirect(url_for("landing"))
        return view(**kwargs)

    return wrapped_view


def is_female():
    return session["userid"][0] == "F"


@app.route("/")
def landing():
    if session.get("userid", None):
        return render_template("landing.html")
    else:
        return render_template("index.html")


@app.route("/signup", methods=("GET", "POST"))
def signup():
    if request.method == "POST":
        name = request.form["name"]
        female = request.form["gender"].lower() == "female"
        phone_no = request.form["phoneNo"]
        vit_mail = request.form["vitMail"]
        password = request.form["password"]

        database = db.get_db()
        crs = database.cursor(dictionary=True)
        error = None
        """
        if x is None:
            error = 'blah blah blah'
        flash(error)
        """
        if error is None:
            crs.execute(
                "INSERT INTO user (email, password, name, female, phone_number) "
                f"VALUES ('{vit_mail}', '{generate_password_hash(password)}', '{name}', {female}, '{phone_no}')"
            )
            database.commit()

        crs.execute("SELECT * FROM user ORDER BY userid DESC LIMIT 1")
        record = crs.fetchone()
        # add else condition in case there was a new record added before this one could be read off the database
        session["userid"] = ("F" if record["female"]
                             else "M") + str(record["userid"])

        return redirect(url_for("landing"))

    return render_template("signup.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        vit_mail = request.form["vitMail"]
        password = request.form["password"]

        database = db.get_db()
        crs = database.cursor(dictionary=True)
        error = None
        """
        if x is None:
            error = 'blah blah blah'
        flash(error)
        """
        if error is None:
            crs.execute(
                f"SELECT userid,password,female FROM user where email='{vit_mail}'"
            )

        record = crs.fetchone()
        if check_password_hash(record["password"], password):

            session["userid"] = ("F" if record["female"] else "M") + str(
                record["userid"]
            )
            return redirect(url_for("landing"))
        else:
            flash("Wrong credentials")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect(url_for('landing'))


@app.route("/cabShare", methods=("GET", "POST"))
@login_required
def cab_share():
    if request.method == "POST":
        pickup_point = request.form["from"]
        drop_point = request.form["to"]
        date = request.form["date"]
        if request.form["time"]:
            date_time = datetime.strptime(
                f"{date} {request.form['time']}", "%Y-%m-%d %H:%M"
            )

        gender_filter = request.form.get("genderFilter", "off") == "on"
        num_people = request.form['numPeople']

        vehicle_types = {"any": 0, "cab": 1, "auto": 2}
        vehicle_type = vehicle_types.get(request.form["vehicleType"], 0)

        database = db.get_db()
        crs = database.cursor(dictionary=True)
        print(f"SELECT * FROM trips WHERE "
              + "resolved!=TRUE AND "
              + (f"(vehicle={vehicle_type} OR vehicle=0) AND " if vehicle_type else "")
              + (f"num_people={num_people} AND " if num_people else "")
              + f"gender_filter={gender_filter} AND "
              + f"pickup_point='{pickup_point}' AND "
              + f"drop_point='{drop_point}' AND "
              + f"trip_date='{date}'")
        crs.execute(
            f"SELECT * FROM trips WHERE "
            + "resolved!=TRUE AND "

            + (f"vehicle={vehicle_type} OR vehicle=0" if vehicle_type else "")
            + f"gender_filter={gender_filter} AND "
            + f"pickup_point='{pickup_point}' AND "
            + f"drop_point='{drop_point}' AND "
            + f"trip_date='{date}'"
        )

        records = crs.fetchall()
        for record in records:
            record["datetime"] = datetime.strptime(
                f"{record['trip_date']} {record['trip_time']}", "%Y-%m-%d %H:%M:%S"
            )

        if request.form["time"]:
            records.sort(key=lambda record: abs(
                record["datetime"] - date_time))
        else:
            records.sort(key=lambda record: record["datetime"])

        for record in records:
            record['trip_time'] = str(record['trip_time'])[:-3]

        return render_template("cabShare.html", form=request.form, records=records, female=is_female())

    database = db.get_db()
    crs = database.cursor(dictionary=True)

    userid = session['userid'][1:]
    crs.execute(f"SELECT * FROM trips WHERE {userid} IN "
                "(user_1, user_2, user_3, user_4, user_5, user_6, user_7, user_8) "
                "AND NOT RESOLVED")
    my_trips = crs.fetchall()
    for trip in my_trips:
        trip['trip_time'] = str(trip['trip_time'])[:-3]

    return render_template('cabShare.html', records=my_trips,
                           locations=load(open('locations.dat', 'rb')), female=is_female())


@app.route("/profile", methods=("GET", "POST"))
@login_required
def profile():
    if request.method == "POST":
        pass

    userid = session["userid"][1:]
    database = db.get_db()
    crs = database.cursor(dictionary=True)

    user_record = crs.execute(f"SELECT * FROM user WHERE userid={userid}")

    return render_template("profile.html", user_record=user_record)


@app.route("/driverDetails")
def driver_details():
    return render_template("driverDetails.html")
