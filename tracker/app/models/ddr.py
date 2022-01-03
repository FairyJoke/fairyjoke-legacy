import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.utils.badges import FCBadges
from app.utils.enumerable import Enumerable


class DDRLocalChart(db.IdMixin, db.Base):
    title = sa.Column(sa.String)
    artist = sa.Column(sa.String)
    step_artist = sa.Column(sa.String)
    difficulty = sa.Column(sa.String)
    level = sa.Column(sa.Integer)


class DDRScore(db.ExScoreMixin, db.Base):
    class Mods(Enumerable):
        TURN = {'MIRROR', 'LEFT', 'RIGHT', 'SHUFFLE'}
        STEP_ZONE = {'OFF'}
        SPEED = set(map(
            lambda x: x / 100,
            [*range(25, 400, 25), *range(400, 800, 50)]
        ))
        ARROW_MOVE = {'BOOST', 'BRAKE', 'WAVE'}
        SCROLL = {'REVERSE'}
        CUT = {
            'ON1', # Only shows 1/4s
            'ON2', # Only shows 1/8s
        }
        FREEZE_ARROW = {'OFF'}
        JUMP = {'OFF'}
        LIFE_GAUGE = {'LIFE4', 'RISKY'}
        SCREEN_FILTER = {'DARK', 'DARKER', 'DARKEST'}
        GUIDELINE = {'BORDER', 'CENTER'}

    class Clears(enum.Enum):
        fail = 'FAIL'
        play = 'PLAYED'
        clear = 'CLEARED'
        fc = 'FULLCOMBO'
        gfc = 'GREAT FULLCOMBO'
        pfc = 'PERFECT FULLCOMBO'
        mfc = 'MARVELOUS FULLCOMBO'

    api_chart_id = sa.Column(sa.Integer)
    local_chart_id = sa.Column(sa.ForeignKey('ddr_local_charts.id'))
    clear_type = sa.Column(sa.Enum(Clears))

    mods = orm.relationship('DDRScoreMod')
    chart = orm.relationship('DDRLocalChart', backref='scores')

    class Badges(FCBadges):
        MFC = 'MARVELOUS FULLCOMBO'
        PFC = 'PERFECT FULLCOMBO'
        GFC = 'GREAT FULLCOMBO'

        @classmethod
        def from_score(cls, score):
            judges = score.judges_obj
            if not judges.good + judges.miss == 0:
                return super().from_score(score)
            if judges.great + judges.perfect == 0:
                return [cls.MFC]
            if judges.great == 0:
                return [cls.PFC]
            return [cls.GFC]

    @property
    def badges(self):
        return self.Badges.from_score(self)


class DDRScoreMod(db.IdMixin, db.Base):
    score_id = sa.Column(sa.ForeignKey('ddr_scores.id'), nullable=False)
    name = sa.Column(sa.Enum(*DDRScore.Mods.keys()), nullable=False)
    value = sa.Column(sa.String)

    score = orm.relationship('DDRScore', back_populates='mods')
