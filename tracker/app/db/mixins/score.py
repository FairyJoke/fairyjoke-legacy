from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm

from app.utils.dictobj import DictObj
from .id import IdMixin

@orm.declarative_mixin
class ScoreMixin(IdMixin):
    @orm.declared_attr
    def user_id(_cls):
        return sa.Column(sa.ForeignKey('users.id'))

    @orm.declared_attr
    def game_id(_cls):
        return sa.Column(sa.ForeignKey('games.id'))

    time = sa.Column(sa.DateTime, default=datetime.utcnow)
    score = sa.Column(sa.Integer)
    judges = sa.Column(sa.JSON, default=dict)
    max_combo = sa.Column(sa.Integer)


    @property
    def judges_obj(self):
        return DictObj(self.judges, default=0)

    @orm.declared_attr
    def user(_cls):
        return orm.relationship('User')

    @orm.declared_attr
    def game(_cls):
        return orm.relationship('Game')


@orm.declarative_mixin
class ExScoreMixin(ScoreMixin):
    ex_score = sa.Column(sa.Integer)
