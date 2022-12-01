from flask import Blueprint, render_template, request, current_app
from backend.utils import find_in_data_folder
import os

stats = Blueprint(__name__, "stats")

@stats.route("/", methods=["GET"])
def players():
    return render_template("stats.html")


@stats.route("/epa", methods=["GET"])
def teams():
    #TODO run a program to move files from backend/EPA to frontend/webapp/static
    file_name = str(request.args.get('id'))
    if file_name == 'None':
        file_name = "schedule_remaining.png"
    return render_template("epa.html", file_name=file_name)
