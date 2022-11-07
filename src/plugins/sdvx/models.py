import sqlalchemy as sa

from fairyjoke import db


# TODO
class Song(db.Base):
    title = sa.Column(sa.String)
