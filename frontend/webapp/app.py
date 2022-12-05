from flask import Flask, render_template
from draft_visualization import draft
from stats_visualization import stats

app = Flask(__name__)
app.register_blueprint(draft, url_prefix="/draft")
app.register_blueprint(stats, url_prefix="/stats")


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
