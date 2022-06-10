from app import db

# create players table with required field
class Players(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(100), nullable = False)
    pos = db.Column(db.String(100), nullable = False)
    team = db.Column(db.String(100), nullable = False)
    stat = db.Column(db.Integer, nullable = True)
    points = db.Column(db.Integer, nullable = False)