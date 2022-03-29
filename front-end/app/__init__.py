from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# set the database uniform resource identifier for the database
app.config["SECRET_KEY"] = '571ebf8e13ca209536c29be68d435c00'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///fantasyfootball.db'

# create an instance of the database module
db = SQLAlchemy(app)

from app import views
from app import models

