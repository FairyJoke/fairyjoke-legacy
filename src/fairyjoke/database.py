from sqlalchemy import func
from sqlalchemy_setup import Database as _Database

from fairyjoke import TMP_PATH
from fairyjoke.pool import Pool


class Database(_Database, Pool):
    def __init__(self, name, **kwargs):
        path = TMP_PATH / f"{name}.db"
        path.parent.mkdir(parents=True, exist_ok=True)
        super().__init__(f"sqlite:///{path}", **kwargs)

    @classmethod
    def _pool_create(cls, key):
        return cls(name=key)
