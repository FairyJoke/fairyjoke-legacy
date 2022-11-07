import sqlalchemy as sa

from fairyjoke import db


class SeriesGroup(db.Base):
    id = sa.Column(sa.String, primary_key=True)
    name = sa.Column(sa.String)


class Series(db.Base):
    id = sa.Column(sa.String, primary_key=True)
    name = sa.Column(sa.String)
    active = sa.Column(sa.Boolean, default=True)
    group_id = sa.Column(sa.ForeignKey("series_groups.id"))

    group = sa.orm.relationship("SeriesGroup", backref="series")


class SeriesRelease(db.Base):
    id = sa.Column(sa.String, primary_key=True, unique=True)
    name = sa.Column(sa.String)
    series_id = sa.Column(sa.ForeignKey("series.id"), nullable=False)
    date = sa.Column(sa.String)
