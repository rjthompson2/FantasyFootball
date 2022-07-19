from flask import Blueprint, render_template, request, current_app
from backend.draft.RunDraft import rundraft_webapp
import selenium

draft = Blueprint(__name__, "draft")

@draft.route("/", methods=['GET'])
def drafter():
    args = request.args
    if 'url' in args.keys():
        #TODO look out for queries which will run code
        url = args['url'].strip()
        #TODO add check for cross site scripting and potential SQL injections
        if url and url != '':
            try:
                current_app.logger.info("Running backend")
                rundraft_webapp(url)
                current_app.logger.info("Backend finished")
            except selenium.common.exceptions.InvalidArgumentException:
                current_app.logger.warning("Selenium exception")
                return render_template("draft.html", error="Please enter a valid url!")
    return render_template("draft.html")


@draft.route("/analysis")
def visualizer():
    return render_template("draft_analysis.html")