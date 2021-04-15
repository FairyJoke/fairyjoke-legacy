from app import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    name_romanized = db.Column(db.String)
    birthday = db.Column(db.DateTime)
    description = db.Column(db.String)
