import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from .difficulty import Difficulties, Difficulty
from .. import router


class Genres(enum.Enum):
    Other = 0
    EXIT_TUNES = 1
    FLOOR = 2
    Touhou = 4
    Vocaloid = 8
    BEMANI = 16
    Original = 32
    Pop_Anime = 64
    Hinabita = 128

    @classmethod
    def from_mask(cls, mask):
        return [
            x
            for x in cls
            if x.value & mask or x.value == mask
        ]

    @classmethod
    def from_name(cls, s: str):
        for x in cls:
            if cls.stringify(x.name) == s:
                return x
        raise KeyError(s)

    @staticmethod
    def stringify(s: str):
        return s.replace('_', ' ')

    def __str__(self):
        return self.stringify(self.name)


class MusicGenre(db.Base):
    __table_prefix__ = router.short_prefix

    music_id = sa.Column(sa.ForeignKey('sdvx_musics.id'), primary_key=True)
    genre = sa.Column(sa.Enum(Genres), primary_key=True)

    music = orm.relationship('Music', back_populates='music_genres')


class Music(db.Base):
    __table_prefix__ = router.short_prefix

    id = sa.Column(sa.Integer, primary_key=True)
    label = sa.Column(sa.String, unique=True)
    title = sa.Column(sa.String)
    title_yomigana = sa.Column(sa.String)
    artist = sa.Column(sa.String)
    artist_yomigana = sa.Column(sa.String)
    ascii = sa.Column(sa.String)
    bpm_min = sa.Column(sa.Float)
    bpm_max = sa.Column(sa.Float)
    release_date = sa.Column(sa.Date)
    background_type = sa.Column(sa.Integer)
    extra_difficulty = sa.Column(sa.Enum(Difficulties))

    # Skipped:
    # volume: u16, all "91"
    # is_fixed: u8, all "1"

    difficulties = orm.relationship('Difficulty', order_by=Difficulty.level, cascade="all, delete-orphan")
    music_genres = orm.relationship('MusicGenre', order_by=MusicGenre.genre, cascade="all, delete-orphan")

    def __init__(self, genre_mask=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for genre in Genres.from_mask(genre_mask):
            db.add(MusicGenre, music_id=self.id, genre=genre)

    def __str__(self):
        return f'{self.artist} - {self.title}'

    @property
    def bpm(self):
        bpm_min, bpm_max = map(
            lambda x: '{:g}'.format(x),
            (self.bpm_min, self.bpm_max),
        )
        if bpm_min == bpm_max:
            return str(bpm_min)
        return f'{bpm_min}-{bpm_max}'

    @property
    def folder(self):
        return f'{str(self.id).zfill(4)}_{self.ascii}'

    @property
    def genres(self):
        return [x.genre for x in self.music_genres]
