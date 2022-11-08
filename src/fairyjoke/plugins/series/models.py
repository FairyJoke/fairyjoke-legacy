import sqlalchemy as sa

from fairyjoke import Plugin


class SeriesGroup(Plugin.db.Base):
    id = sa.Column(sa.String, primary_key=True)
    name = sa.Column(sa.String)


class Series(Plugin.db.Base):
    id = sa.Column(sa.String, primary_key=True)
    name = sa.Column(sa.String)
    translation = sa.Column(sa.String)
    active = sa.Column(sa.Boolean, default=True)
    group_id = sa.Column(sa.ForeignKey("series_groups.id"))

    group = sa.orm.relationship("SeriesGroup", backref="series")


class SeriesGame(Plugin.db.Base):
    id = sa.Column(sa.String, primary_key=True)
    series_id = sa.Column(sa.ForeignKey("series.id"), primary_key=True, nullable=False)
    name = sa.Column(sa.String)
    date = sa.Column(sa.String)

    series = sa.orm.relationship("Series", backref="series")
