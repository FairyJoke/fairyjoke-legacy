import sqlalchemy as sa

from app import db


class Game(db.IdMixin, db.Base):
    api_id = sa.Column(sa.Integer)
    name = sa.Column(sa.String)
