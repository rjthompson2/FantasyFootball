from flask import render_template, request
from app import app
from app import db
from app.models import Players


@app.route("/")
def home():
    return "<b>Hello World!</b>"


@app.route("/template")
def template():
    return render_template("home.html")


@app.route("/players", methods=["GET", "POST"])
def players():
    # check the request method to ensure the handling of POST request only
    if request.method == "POST":
        # store the form value
        user_name = request.form["username"]
        pos = request.form["email"]
        team = request.form["password"]

        # create an instance of the user table
        user = Players(name=user_name, pos=pos, team=team)

        return username + " <br/> " + team
    return render_template("players.html")


# @app.route('/draft')
# def draft():
#     return render_template('draft.html')
