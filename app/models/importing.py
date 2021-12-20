from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class ImportBatch(db.IdMixin, db.Base):
    version_id = sa.Column(sa.ForeignKey('versions.id'))
    ran_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    comment = sa.Column(sa.String)

    version = orm.relationship('Version', backref='imports')
