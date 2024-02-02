import enum

import sqlalchemy as sa
from app import db
from sqlalchemy import orm

from .difficulty import SDVXDifficulties, SDVXDifficulty


class SDVXGenres(enum.Enum):
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
        return [x for x in cls if x.value & mask or x.value == mask]

    @classmethod
    def from_name(cls, s: str):
        for x in cls:
            if cls.stringify(x.name) == s:
                return x
        raise KeyError(s)

    @staticmethod
    def stringify(s: str):
        return s.replace("_", " ")

    def __str__(self):
        return self.stringify(self.name)


class SDVXMusicGenre(db.IdMixin, db.Base):
    music_id = sa.Column(sa.ForeignKey("sdvx_musics.id"))
    genre = sa.Column(sa.Enum(SDVXGenres))

    music = orm.relationship("SDVXMusic", back_populates="music_genres")


class SDVXMusic(db.BpmMixin, db.Base):
    id = sa.Column(sa.Integer, primary_key=True)
    label = sa.Column(sa.String, unique=True)
    title = sa.Column(sa.String)
    title_yomigana = sa.Column(sa.String)
    artist = sa.Column(sa.String)
    artist_yomigana = sa.Column(sa.String)
    ascii = sa.Column(sa.String)
    release_date = sa.Column(sa.Date)
    background_type = sa.Column(sa.Integer)
    extra_difficulty = sa.Column(sa.Enum(SDVXDifficulties))
    version = sa.Column(sa.Integer)

    # Skipped:
    # volume: u16, all "91"
    # is_fixed: u8, all "1"

    difficulties = orm.relationship(
        "SDVXDifficulty",
        order_by=SDVXDifficulty.level,
        cascade="all, delete-orphan",
    )
    music_genres = orm.relationship(
        "SDVXMusicGenre",
        order_by=SDVXMusicGenre.genre,
        cascade="all, delete-orphan",
    )

    def __init__(self, genre_mask=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if genre_mask:
            self.music_genres = [
                SDVXMusicGenre(music=self, genre=genre)
                for genre in SDVXGenres.from_mask(genre_mask)
            ]

    def __str__(self):
        return f"{self.artist} - {self.title}"

    @property
    def folder(self):
        return f"{str(self.id).zfill(4)}_{self.ascii}"

    @property
    def genres(self):
        return [x.genre for x in self.music_genres]
