from app import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    platform_id = db.relationship(db.Integer, db.ForeignKey('platform.id'))
    main = db.Column(db.Boolean)
    description = db.Column(db.String)

    releases = db.relationship('Release', backref='game', lazy='dynamic')
    charts = db.relationship('Chart', backref='game', lazy='dynamic')

class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(2))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    date = db.Column(db.DateTime)
    description = db.Column(db.String)

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    games = db.relationship('Game', backref='platform', lazy='dynamic')

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    name_localized = db.Column(db.String)
    description = db.Column(db.String)

    games = db.relationship('Game', backref='series', lazy='dynamic')
