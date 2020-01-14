from app import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    title = db.Column(db.String)
    title_romanized = db.Column(db.String)
    title_localized = db.Column(db.String)
    main_bpm = db.Column(db.Integer)
    low_bpm = db.Column(db.Integer)
    high_bpm = db.Column(db.Integer)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    name = db.Column(db.String)
    name_romanized = db.Column(db.String)
    name_localized = db.Column(db.String)
    description = db.Column(db.String)

    songs = db.relationship('Song', backref='artist', lazy='dynamic')

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    name_localized = db.Column(db.String)
    birthday = db.Column(db.DateTime)
    description = db.Column(db.String)

    aliases = db.relationship('Artist', backref='person', lazy='dynamic')
