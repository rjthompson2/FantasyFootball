from flask import Blueprint, render_template, request, current_app
from backend.utils import find_in_data_folder
from backend.epa import plot
from backend import CollectPlayerDataTimeSeries
import pandas as pd
import shutil
import time
import datetime
import os

stats = Blueprint(__name__, "stats")


@stats.route("/", methods=["GET", "POST"])
def players():
    file_name = str(request.args.get("id"))
    year = "2022"
    df = ""

    if request.method == 'POST': 
        year = str(request.form['year'])

    if file_name != "None":
        file_name = "backend/data/"+file_name+year+".csv"

        if year == "2022":
            file_time = time.ctime(
                os.path.getmtime(file_name)
            ).split()
            now = time.asctime(time.localtime()).split()
            if now[2] != file_time[2]:
                CollectPlayerDataTimeSeries.main(int(year))

        df = pd.read_csv(file_name).sort_values(by=['AVG'], ascending=False).reset_index(drop=True).to_html()
    return render_template("stats.html", df=df)


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
