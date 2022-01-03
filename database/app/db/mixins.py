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

@orm.declarative_mixin
class BpmMixin:
    bpm_min = sa.Column(sa.Float)
    bpm_max = sa.Column(sa.Float)

    @property
    def bpm(self):
        bpm_min, bpm_max = map(
            lambda x: '{:g}'.format(x) if x is not None else None,
            (self.bpm_min, self.bpm_max),
        )
        if not bpm_max:
            return bpm_min
        if not bpm_min:
            return bpm_max
        if bpm_min == bpm_max:
            return str(bpm_min)
        return f'{bpm_min}-{bpm_max}'
