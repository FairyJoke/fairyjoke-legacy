import sqlalchemy as sa

from app import db


class User(db.IdMixin, db.Base):
    handle = sa.Column(sa.String, nullable=None)
    display_name = sa.Column(sa.String)
    hashed_password = sa.Column(sa.String)
