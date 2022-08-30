from flask import Flask, render_template
from draft_visualization import draft

app = Flask(__name__)
app.register_blueprint(draft, url_prefix="/draft")


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
