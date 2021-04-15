from app import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # person = db.relationship('Person', backref='aliases', lazy='dynamic')
    name = db.Column(db.String)
    name_romanized = db.Column(db.String)
    name_localized = db.Column(db.String)
    description = db.Column(db.String)
