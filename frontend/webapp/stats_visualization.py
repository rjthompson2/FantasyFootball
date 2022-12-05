from flask import Blueprint, render_template, request, current_app
from backend.utils import find_in_data_folder
from backend.epa import plot
import shutil
import time
import datetime
import os

stats = Blueprint(__name__, "stats")


@stats.route("/", methods=["GET"])
def players():
    return render_template("stats.html")


@stats.route("/epa", methods=["GET"])
def teams():
    file_name = str(request.args.get("id"))
    if file_name == "None":
        file_name = "schedule_remaining.png"

    src = find_in_data_folder("EPA/" + file_name)
    # Copies file into static folder if it isn't already in there
    if not os.path.exists("frontend/webapp/static/" + file_name):
        shutil.copy(src, "frontend/webapp/static")
        return render_template("epa.html", file_name=file_name)

    # Updates plots
    file_time = time.ctime(
        os.path.getmtime("frontend/webapp/static/" + file_name)
    ).split()
    now = time.asctime(time.localtime()).split()
    if now[2] != file_time[2]:
        # TODO figure out auto updates
        # plot.make_all([int(now[-1])])
        shutil.copy(src, "frontend/webapp/static")

    return render_template("epa.html", file_name=file_name)
