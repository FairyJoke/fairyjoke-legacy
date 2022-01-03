from typing import Type
import sqlalchemy as sa
from sqlalchemy import orm, MetaData
from sqlalchemy.engine import Engine
import sqlalchemy_utils as sa_utils

from app import config
from .base import Base as CustomBase


meta = MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
})

Base: Type = orm.declarative_base(cls=CustomBase, metadata=meta)
engine: Engine = sa.create_engine(config.DB_URI)
Session = orm.sessionmaker(bind=engine, autoflush=False)
session = Session()

if not sa_utils.database_exists(engine.url):
    sa_utils.create_database(engine.url)

from .actions import add, create
from .mixins import IdMixin, ImportMixin, BpmMixin
from .pagination import paginate
