import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Series(db.Base):
    name = sa.Column(sa.String)
    short = sa.Column(sa.String, primary_key=True)

    has_api = sa.Column(sa.Boolean)


class Game(db.Base):
    name = sa.Column(sa.String)
    short = sa.Column(sa.String, primary_key=True)
    series_short = sa.Column('series', sa.ForeignKey('series.short'), primary_key=True)

    def __str__(self):
        return self.name


class Version(db.IdMixin, db.Base):
    name = sa.Column(sa.String)
    game_short = sa.Column('game', sa.ForeignKey('games.short'))
    series_short = sa.Column('series', sa.ForeignKey('series.short'))

    game = orm.relationship('Game')
