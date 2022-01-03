import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class DDRPlaystyles(enum.Enum):
    SP = 'Single'
    DP = 'Double'


class DDRDifficulties(enum.Enum):
    BEGINNER = 0
    BASIC = 1
    DIFFICULT = 2
    EXPERT = 3
    CHALLENGE = 4

    @property
    def short(self):
        if self == self.BEGINNER:
            return 'b'
        return self.name[0]


class DDRDifficulty(db.IdMixin, db.Base):
    music_id = sa.Column(sa.ForeignKey('ddr_musics.id'))
    playstyle = sa.Column(sa.Enum(DDRPlaystyles))
    level = sa.Column(sa.Integer)
    diff = sa.Column(sa.Enum(DDRDifficulties))

    music = orm.relationship('DDRMusic', back_populates='difficulties')

    def __str__(self):
        return f'{self.short} {self.level}'

    @property
    def name(self):
        return self.diff.name

    @property
    def short(self):
        return f'{self.diff.short}{self.playstyle.name}'

    @property
    def full(self):
        return f'{self.diff.name} {self.playstyle.name} {self.level}'

    @property
    def sort(self):
        return self.diff.value + (5 * (self.playstyle == DDRPlaystyles.DP))


class DDRDifficultyImport(db.ImportMixin, db.Base):
    difficulty_id = sa.Column(sa.ForeignKey('ddr_difficulties.id'))

    difficulty = orm.relationship('DDRDifficulty', backref='imports')
