from flask import Blueprint, render_template, request, current_app
from backend.utils import find_in_data_folder
from backend.epa import plot
from backend import CollectPlayerDataTimeSeries, utils
import pandas as pd
import shutil
import time
import datetime
import os

stats = Blueprint(__name__, "stats")


@stats.route("/", methods=["GET", "POST"])
def players():
    original = str(request.args.get("id"))
    year = "2022"
    df = ""
    team = None

    if request.method == 'POST': 
        if 'year' in request.form:
            year = str(request.form['year'])
        if 'groupby' in request.form:
            team = str(request.form['groupby'])


    html = ""
    if original != "None":
        file_name = "backend/data/"+original+year+".csv"

        if year == "2022":
            file_time = time.ctime(
                os.path.getmtime(file_name)
            ).split()
            now = time.asctime(time.localtime()).split()
            if now[2] != file_time[2]:
                CollectPlayerDataTimeSeries.main(int(year))
        
        df = pd.read_csv(file_name).sort_values(by=['AVG'], ascending=False).reset_index(drop=True)
        if team:
            for team_name in list(utils.Teams):
                # html += team_name.value
                html += "<a href=plot?id=wopr&year="+year+"&team="+team_name.value+">"+team_name.value+"</a>"
                html += df[df['TEAM'] == team_name.value].to_html()

        else:
            html = df.to_html()
    return render_template("stats.html", df=html)


@stats.route("/plot")
def player_plots():
    name = str(request.args.get("id"))
    year = str(request.args.get("year"))
    team = str(request.args.get("team"))
    if name == "None":
        button = '<form method="get" action="/stats"  method="post"><button type="submit">Back</button></form>'
        return render_template("stats.html")

    folder = "WeeklyTeam"
    src = ""
    button = '<form method="get" action="/stats/?id='+name+'_"><button type="submit" groupby="True">Back</button></form>'

    file_name = year + "_" + team + "_" + name + ".png"
    # team = str(request.args.get("team"))
    if name == "wopr":
        src = find_in_data_folder(folder+"WOPR/" + file_name)
    
    
    html = '<img src="/static/'+file_name+'" alt="statistics for each team based on the stat. ERROR '+file_name+' not found!" style="width:800px;height:600px;"></img>'

    # Copies file into static folder if it isn't already in there
    if not os.path.exists("frontend/webapp/static/" + file_name):
        shutil.copy(src, "frontend/webapp/static")
        return render_template("stats_plot.html", df=html, button=button)

    # Updates plots
    file_time = time.ctime(
        os.path.getmtime("frontend/webapp/static/" + file_name)
    ).split()
    now = time.asctime(time.localtime()).split()
    if now[2] != file_time[2]:
        # TODO figure out auto updates
        # plot.make_all([int(now[-1])])
        shutil.copy(src, "frontend/webapp/static")

    return render_template("stats_plot.html", df=html, button=button)

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
