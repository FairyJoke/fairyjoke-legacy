import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from .. import router



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

    @property
    def games(self):
        return {x.batch.version.game for x in self.imports}


class ApecaImport(db.ImportMixin, db.Base):
    __table_prefix__ = router.short_prefix

    apeca_id = sa.Column(sa.ForeignKey('sdvx_apecas.id'))

    apeca = orm.relationship('Apeca', backref='imports')
