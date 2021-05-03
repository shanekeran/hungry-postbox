import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_paginate import Pagination, get_page_args
from datetime import datetime
import smtplib
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
users = list(range(100))

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config["EMAIL_ADDRESS"] = os.environ.get("EMAIL_ADDRESS")
app.config["PASSWORD"] = os.environ.get("PASSWORD")

mongo = PyMongo(app)


# Pagination functions.
# Credit https://github.com/Edb83/self-isolution/blob/master/app.py

PER_PAGE = 12  # Maximum 12 members displayed per page


def paginated(members):
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    offset = page * PER_PAGE - PER_PAGE

    return members[offset: offset + PER_PAGE]


def pagination_args(members):
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    total = len(members)

    return Pagination(page=page, per_page=PER_PAGE, total=total)

# Calculates age of member based on their DOB
# Helped by Stack Overflow, link in README.


def calculate_age(born):
    dob = datetime.strptime(born, '%d/%m/%Y').date()
    today_string = datetime.today().strftime('%d/%m/%Y')
    today_date = datetime.strptime(today_string, '%d/%m/%Y').date()
    age = int((today_date - dob).days/365)
    return(age)


@app.route("/")
@app.route("/home")
def home_page():
    # Credit to Stack Overflow user "dbam" https://stackoverflow.com/questions/2824157/random-record-from-mongodb
    random_members = mongo.db.members.aggregate([{"$sample": {"size": 3}}])
    
    return render_template("index.html", random_members=random_members,
                           calculate_age=calculate_age)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Checks if the username is already in use
        existing_member = mongo.db.members.find_one(
            {"username": request.form.get("username").lower()})

        existing_email = mongo.db.members.find_one(
            {"email": request.form.get("email")})

        if existing_member:
            flash("Username already exists")
            return redirect(url_for("register",
                                    _external=True, _scheme="https"))
        
        if existing_email:
            flash("Email already in use")
            return redirect(url_for("register",
                                    _external=True, _scheme="https"))

        # If username is available, this creates an account in the db.
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email").lower(),
            "dob": request.form.get("dob"),
            "gender": request.form.get("gender"),
            "nationality": request.form.get("nationality"),
            "country": request.form.get("country"),
            "description": request.form.get("description"),
            "looking_for": request.form.get("looking_for"),
            "picture": request.form.get("picture")
        }
        mongo.db.members.insert_one(register)


        # Put the registered user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Account created")
        return redirect(url_for("home_page", username=session["user"],
                                _external=True, _scheme="https"))
    return render_template("register.html")


@app.route("/edit_profile/<member_id>", methods=["GET", "POST"])
def edit_profile(member_id):
    if request.method == "POST":
        #checks for existing username on db
        existing_member = mongo.db.members.find_one(
            {"username": request.form.get("username").lower()})
        #checks for existing email on db
        existing_email = mongo.db.members.find_one(
            {"email": request.form.get("email")})
        
        # Flash message if user inputs a username that's already taken
        # Flash message doesn't show if user reinputs their current username
        if existing_member:
            current_username = mongo.db.members.find_one(
                {"username": session["user"]})
            if existing_member != current_username:
                flash("Username already in use")
                return redirect(url_for("edit_profile",
                                        _external=True, _scheme="https"))

        # Flash message if user inputs an email address that's already taken
        # Flash message doesn't show if user reinputs their current email
        if existing_email:
            current_email = mongo.db.members.find_one(
                {"username": session["user"]})["email"]
            if request.form.get("email") != current_email:
                flash("Email already in use")
                return redirect(url_for("home_page",
                                        _external=True, _scheme="https"))


        # If username is available, this creates an account in the db.
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email").lower(),
            "dob": request.form.get("dob"),
            "gender": request.form.get("gender"),
            "nationality": request.form.get("nationality"),
            "country": request.form.get("country"),
            "description": request.form.get("description"),
            "looking_for": request.form.get("looking_for"),
            "picture": request.form.get("picture")
        }

        # Changes the session cookie to the new username, if it was edited.
        session["user"] = request.form.get("username").lower()
        # Updates user profile in db
        mongo.db.members.update({"_id": ObjectId(member_id)}, register)
        user_profile = mongo.db.members.find_one({"username": session["user"]})
        return redirect(url_for("home_page", username=session["user"],
                                user_profile=user_profile,
                                _external=True, _scheme="https"))

    member = mongo.db.members.find_one({"_id": ObjectId(member_id)})
    user_profile = mongo.db.members.find_one({"username": session["user"]})
    
    return render_template("edit_profile.html", member=member)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Checks if the username is already in use
        existing_member = mongo.db.members.find_one(
            {"username": request.form.get("username").lower()})

        if existing_member:
            # Checks submitted password matches password in db
            if check_password_hash(
                existing_member['password'], request.form.get('password')):
                session["user"] = request.form.get("username").lower()
                #  flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"],
                                _external=True, _scheme="https"))
            else:
                #invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login",
                                _external=True, _scheme="https"))

        else:
            # Username not found
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login",
                                    _external=True, _scheme="https"))


    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if session["user"]:

        # Retrieve the session user's username from db
        username = mongo.db.members.find_one(
            {"username": session["user"]})["username"]
        # Retrieve user details from db
        member = mongo.db.members.find_one({"username": session["user"]})

        return render_template("profile.html", username=username,
                               member=member, calculate_age=calculate_age)

    if "user" not in session:
        return redirect(url_for("login.html", _external=True, _scheme="https"))


@app.route("/delete_account/<member_id>")
def delete_account(member_id):
    mongo.db.members.remove({"_id": ObjectId(member_id)})
    session.clear()  # logs out user
    flash("Account Successfully Deleted")
    return redirect(url_for("home_page",_external=True, _scheme="https"))


@app.route("/logout")
def logout():
    # Logs user out by removing session cookie and redirecting back to login.
    flash("Successfully logged out")
    session.pop("user")
    return redirect(url_for("login",_external=True, _scheme="https"))


@app.route("/members")
def members():
    # Retrieves all members from db, sorted newest to oldest
    members = list(mongo.db.members.find().sort('_id', -1))
    # Paginates results
    members_paginated = paginated(members)
    pagination = pagination_args(members)

    return render_template("members.html", members=members_paginated,
                           pagination=pagination, calculate_age=calculate_age)


@app.route("/member_profile/<member_id>")
def member_profile(member_id):
    member = mongo.db.members.find_one({"username": member_id})

    return render_template("profile.html", member=member,
                           calculate_age=calculate_age)


@app.route("/contact/<member_id>")
def contact(member_id):
    member = mongo.db.members.find_one({"username": member_id})
    user = mongo.db.members.find_one({"username": session["user"]})

    # Email functionality
    # Credit: LucidProgramming on YouTube (link in README)
    def send_email(subject, message):
        try:
            server = smtplib.SMTP("smtp.gmail.com:587")
            server.ehlo()
            server.starttls()
            server.login(app.config["EMAIL_ADDRESS"],
                         app.config["PASSWORD"])
            message = "Subject: {}\n\n{}".format(subject, message)
            server.sendmail(app.config["EMAIL_ADDRESS"],
                            member["email"], message)
            server.quit()
            flash("User contacted successfully.")
        except:
            flash("Unable to contact user, try again later")
    # Email subject
    subject = "PenPal request"
    # Email content. Recipient will be given the users username, email and URL
    message = ("Greetings from Hungry Postbox,"
               " {} would like to connect with you.\n"
               "You can contact this user at {}.\n"
               "We reccomend first viewing their profile linked below.\n\n"
               "http://hungry-postbox.herokuapp.com/profile/{}"
               ).format(user['username'], user['email'], user['username'])

    send_email(subject, message)
    return redirect(url_for("home_page", username=session["user"],
                            _external=True, _scheme="https"))


# Error handlers for 404/500 errors.
@app.errorhandler(404)
def no_page_found(error):
    return render_template('error.html', error=error), 400

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error=error), 500

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)     # Set to False b4 submission.
