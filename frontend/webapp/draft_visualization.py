from flask import Blueprint, render_template

draft = Blueprint(__name__, "draft")

@draft.route("/")
def drafter():
    return render_template("draft.html")


@draft.route("/analysis")
def visualizer():
    return render_template("draft_analysis.html")