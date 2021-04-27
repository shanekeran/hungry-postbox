import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")


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
            return redirect(url_for("register"))
        
        if existing_email:
            flash("Email already in use")
            return redirect(url_for("register"))

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
        return redirect(url_for("home_page", username=session["user"]))
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
                return redirect(url_for("edit_profile"))

        # Flash message if user inputs an email address that's already taken
        # Flash message doesn't show if user reinputs their current email
        if existing_email:
            current_email = mongo.db.members.find_one(
                {"username": session["user"]})["email"]
            if request.form.get("email") != current_email:
                flash("Email already in use")
                return redirect(url_for("home_page"))

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
                                user_profile=user_profile))

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
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                #invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # Username not found
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))


    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    #Retrieve the session user's username from db
    username = mongo.db.members.find_one(
        {"username": session["user"]})["username"]
    #Retrieve user details from db
    user_profile = mongo.db.members.find_one({"username": session["user"]})

    
    if session["user"]:
        return render_template("profile.html", username=username,
                                user_profile=user_profile)
    
    return redirect(url_for("login.html"))


@app.route("/delete_account/<member_id>")
def delete_account(member_id):
    mongo.db.members.remove({"_id": ObjectId(member_id)})
    session.clear()  # logs out user
    flash("Account Successfully Deleted")
    return redirect(url_for("home_page"))


@app.route("/logout")
def logout():
    # Logs user out by removing session cookie and redirecting back to login.
    flash("Successfully logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/members")
def members():
    members = list(mongo.db.members.find())
    return render_template("members.html", members=members)


@app.route("/member_profile/<member>")
def member_profile(member):
    user_profile = mongo.db.members.find_one({"username": member})
    return render_template("profile.html", user_profile=user_profile)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)     # Set to False b4 submission.
