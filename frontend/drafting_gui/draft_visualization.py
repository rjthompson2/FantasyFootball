from flask import Blueprint, render_template

draft = Blueprint(__name__, "draft")

@draft.route("/")
def home():
    return render_template("draft.html")