from app import db


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship('Artist', backref='songs')
    title = db.Column(db.String)
    title_romanized = db.Column(db.String)
    title_localized = db.Column(db.String)
    main_bpm = db.Column(db.Integer)
    min_bpm = db.Column(db.Integer)
    max_bpm = db.Column(db.Integer)
