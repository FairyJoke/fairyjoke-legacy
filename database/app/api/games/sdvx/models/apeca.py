import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class SDVXApeca(db.Base):
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


class SDVXApecaImport(db.ImportMixin, db.Base):
    apeca_id = sa.Column(sa.ForeignKey('sdvx_apecas.id'))

    apeca = orm.relationship('SDVXApeca', backref='imports')
