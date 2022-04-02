import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Series(db.Base):
    name = sa.Column(sa.String, nullable=False)
    short = sa.Column(sa.String, primary_key=True)

    has_api = sa.Column(sa.Boolean)

    games = orm.relationship('Game', order_by='Game.sort')

    def __str__(self):
        return self.name


class Game(db.IdMixin, db.Base):
    name = sa.Column(sa.String, nullable=False)
    short = sa.Column(sa.String, unique=True)
    series_short = sa.Column('series', sa.ForeignKey('series.short'))
    sort = sa.Column(sa.Integer)

    series = orm.relationship('Series', back_populates='games')
    versions = orm.relationship('Version')

    def __str__(self):
        return self.name


class Version(db.IdMixin, db.Base):
    name = sa.Column(sa.String)
    game_id = sa.Column(sa.ForeignKey('games.id'))

    game = orm.relationship('Game', back_populates='versions')
