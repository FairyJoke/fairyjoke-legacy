import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class DDRMusic(db.BpmMixin, db.Base):
    SERIES_TO_GAME = {
        1: '1st',
        2: '2nd',
        3: '3rd',
        4: '4th',
        5: '5th',
        6: 'MAX',
        7: 'MAX2',
        8: 'EXTREME',
        9: 'SN',
        10: 'SN2',
        11: 'X',
        12: 'X2',
        13: 'X3',
        14: '2013',
        15: '2014',
        16: '2014',
        17: 'Ace',
        18: 'A20',
        19: 'A20+',
    }

    id = sa.Column(sa.Integer, primary_key=True)
    label = sa.Column(sa.String, unique=True)
    title = sa.Column(sa.String)
    title_yomigana = sa.Column(sa.String)
    artist = sa.Column(sa.String)
    series = sa.Column(sa.Integer)
    bemani = sa.Column(sa.Integer)
    background_type = sa.Column(sa.Integer)

    def __str__(self):
        return f'{self.artist} - {self.title}'

    difficulties = orm.relationship('DDRDifficulty')

    @property
    def game(self):
        from app.models import Game
        if not (short := self.SERIES_TO_GAME.get(self.series)):
            return None
        return db.session.query(Game).filter_by(short=short, series_short='ddr').first()

    @property
    def sorted_difficulties(self):
        return sorted(self.difficulties, key=lambda x: x.sort)

    @property
    def fixed_difficulties(self):
        from .difficulty import DDRDifficulties, DDRDifficulty, DDRPlaystyles
        return {
            style.name: [
                (
                    db.session.query(DDRDifficulty)
                    .filter_by(music=self, diff=diff, playstyle=style)
                ).first()
                for diff in DDRDifficulties
            ] for style in DDRPlaystyles
        }
