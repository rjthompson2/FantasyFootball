from flask import Blueprint, render_template, request, current_app
from backend.utils import find_in_data_folder
import shutil
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
    move_file('EPA/'+file_name)
    return render_template("epa.html", file_name=file_name)

def move_file(file_name, destination='frontend/webapp/static'):
    src = find_in_data_folder(file_name)
    shutil.copy(src, destination)