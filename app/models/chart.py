from app import db

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    difficulty_id = db.Column(db.Integer, db.ForeignKey('difficulty.id'))
    internal_id = db.Column(db.Integer)
    bpm_display = db.Column(db.String)
    level = db.Column(db.String)

    level_changes = db.relationship(
        'Difficulty',
        backref='chart',
        lazy='dynamic'
    )
    series_specific = db.relationship(
        'SeriesSpecificChartValue',
        backref='chart',
        lazy='dynamic'
    )

class Difficulty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    internal_id = db.Column(db.Integer)
    order = db.Column(db.Integer)
    bg_color = db.Column(db.Integer)
    fg_color = db.Column(db.Integer)
    name = db.Column(db.String)

    charts = db.relationship('Chart', backref='difficulty', lazy='dynamic')

class LevelChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chart_id = db.Column(db.Integer, db.ForeignKey('chart.id'))
    previous_value = db.Column(db.String)
    date = db.Column(db.DateTime)

class SeriesSpecificChartProperty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    name = db.Column(db.String)

    values = db.relationship(
        'SeriesSpecificChartValue',
        backref='property',
        lazy='dynamic'
    )

class SeriesSpecificChartValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(
        db.Integer,
        db.ForeignKey('series_specific_chart_property.id')
    )
    chart_id = db.Column(db.Integer, db.ForeignKey('chart.id'))
    value = db.Column(db.String)
