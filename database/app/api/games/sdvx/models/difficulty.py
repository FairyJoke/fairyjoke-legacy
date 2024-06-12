import enum

import sqlalchemy as sa
from app import db
from sqlalchemy import orm


class SDVXDifficulties(enum.Enum):
    NOV = "NOVICE"
    ADV = "ADVANCED"
    EXH = "EXHAUST"
    MXM = "MAXIMUM"

    INF = "INFINITE"
    GRV = "GRAVITY"
    HVN = "HEAVENLY"
    VVD = "VIVID"
    XCD = "EXCEED"

    def __int__(self):
        return {
            self.NOV: 1,
            self.ADV: 2,
            self.EXH: 3,
            self.MXM: 5,
        }.get(self, 4)

    def __str__(self):
        return self.name


class SDVXDifficulty(db.IdMixin, db.Base):
    music_id = sa.Column(sa.ForeignKey("sdvx_musics.id"))
    diff = sa.Column("name", sa.Enum(SDVXDifficulties))
    level = sa.Column(sa.Integer)
    illustrator = sa.Column(sa.String)
    effector = sa.Column(sa.String)
    jacket_id = sa.Column(sa.Integer)

    # Skipped:
    # price: s32, version dependent
    # limited: u8, version dependent
    # jacket_print: s32, idk
    # jacket_mask: s32, idk

    music = orm.relationship("SDVXMusic", back_populates="difficulties")

    has_internal_jacket = sa.Column(sa.Boolean)
    external_jacket = sa.Column(sa.String)

    def __str__(self):
        return f"{self.music} [{self.name}]"

    @property
    def name(self):
        return f"{self.diff} {self.level}"

    @property
    def full(self):
        return f"{self.diff.value} {self.level}"

    def get_filename(self, jacket_id=False, size=None):
        jacket_id = jacket_id or self.jacket_id
        stem = f"jk_{str(self.music_id).zfill(4)}_{jacket_id}"
        if size:
            stem += f"_{size}"
        return f"{stem}.png"

    @property
    def filename(self):
        return self.get_filename()

    @property
    def games(self):
        return {x.batch.version.game for x in self.imports}

    imports = orm.relationship("SDVXDifficultyImport")


class SDVXDifficultyImport(db.ImportMixin, db.Base):
    difficulty_id = sa.Column(sa.ForeignKey("sdvx_difficulties.id"))

    difficulty = orm.relationship("SDVXDifficulty", back_populates="imports")
