import sqlalchemy as sa
from sqlalchemy import orm


@orm.declarative_mixin
class IdMixin:
    id = sa.Column(sa.Integer, primary_key=True)


@orm.declarative_mixin
class ImportMixin(IdMixin):
    @orm.declared_attr
    def backref_name(cls):
        return f'{cls.__tablename__}_imports'

    @orm.declared_attr
    def batch_id(_cls):
        return sa.Column(sa.ForeignKey('import_batches.id'))

    @orm.declared_attr
    def batch(cls):
        return orm.relationship('ImportBatch', backref=cls.backref_name)
