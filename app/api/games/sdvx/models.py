import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from . import router


GENRES = {
    0: 'Other',
    1: 'EXIT TUNES',
    2: 'FLOOR',
    4: 'Touhou',
    8: 'Vocaloid',
    16: 'BEMANI',
    32: 'Original',
    64: 'Pop/Anime',
    128: 'Hinabita',
}


class Difficulties(enum.Enum):
    NOV = 'NOVICE'
    ADV = 'ADVANCED'
    EXH = 'EXHAUST'
    MXM = 'MAXIMUM'

    INF = 'INFINITE'
    GRV = 'GRAVITY'
    HVN = 'HEAVENLY'
    VVD = 'VIVID'

    def __int__(self):
        return {
            self.NOV: 1,
            self.ADV: 2,
            self.EXH: 3,
            self.MXM: 5,
        }.get(self, 4)

    def __str__(self):
        return self.name


class Difficulty(db.Base):
    __table_prefix__ = router.short_prefix

    music_id = sa.Column(sa.ForeignKey('sdvx_musics.id'), nullable=False, primary_key=True)
    name = sa.Column(sa.Enum(Difficulties), primary_key=True)
    level = sa.Column(sa.Integer)
    illustrator = sa.Column(sa.String)
    effector = sa.Column(sa.String)
    jacket_id = sa.Column(sa.Integer)

    # Skipped:
    # price: s32, version dependent
    # limited: u8, version dependent
    # jacket_print: s32, idk
    # jacket_mask: s32, idk

    music = orm.relationship('Music', back_populates='difficulties')

    def __str__(self):
        return f'{self.name}{self.level}'

    def get_filename(self, jacket_id=False, size=None):
        jacket_id = jacket_id or self.jacket_id
        stem = f'jk_{str(self.music_id).zfill(4)}_{jacket_id}'
        if size:
            stem += f'_{size}'
        return f'{stem}.png'

    @property
    def filename(self):
        return self.get_filename()


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
    genre = sa.Column(sa.Integer)
    extra_difficulty = sa.Column(sa.Enum(Difficulties))

    # Skipped:
    # volume: u16, all "91"
    # is_fixed: u8, all "1"

    difficulties = orm.relationship('Difficulty', order_by=Difficulty.level)

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
        return [
            value
            for key, value in GENRES.items()
            if key & self.genre
        ]


class Apeca(db.Base):
    __table_prefix__ = router.short_prefix

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    texture = sa.Column(sa.String)
    illustrator = sa.Column(sa.String)
    rarity = sa.Column(sa.Integer)
    sort = sa.Column(sa.Integer)
    generator = sa.Column(sa.Integer)
    genre = sa.Column(sa.Integer)
    messages = sa.Column(sa.JSON)

    # Skipped:
    # distribution_date: u32, weird format, often 0
    # limited
