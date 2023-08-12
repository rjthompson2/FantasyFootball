from flask import Blueprint, render_template, request, current_app
from backend.utils import find_in_data_folder, find_parent_dir
from backend.data_collection.utils import get_season_year
from backend.events.simple_listener import write
import pandas as pd
import selenium
import asyncio
import shutil
import os

draft = Blueprint(__name__, "draft")

@draft.route("/", methods=["GET"])
def drafter():
    args = request.args
    if "url" in args.keys():
        # TODO look out for queries which will run code
        url = args["url"].strip()
        # TODO add check for cross site scripting and potential SQL injections
        if url and url != "":
            try:
                current_app.logger.info("Running backend")
                # Creates a copy of the drafting data
                year = get_season_year()
                copy = pd.read_csv(find_in_data_folder(f"draft_order_{year}.csv"))
                new_path = find_in_data_folder(f"draft_order_{year}_copy.csv")
                copy.to_csv(new_path, index=False)

                # Runs draft
                asyncio.run(write("RunDraft", [url, 1]))
                current_app.logger.info("Backend finished")
            except selenium.common.exceptions.InvalidArgumentException:
                current_app.logger.warning("Selenium exception")
                return render_template("draft.html", error="Please enter a valid url!")
    return render_template("draft.html")

@draft.route("/analysis")
def visualizer():
    return render_template("draft_analysis.html")
