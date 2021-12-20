from typing import Type
import sqlalchemy as sa
from sqlalchemy import orm


def camel_to_snake(s: str) -> str:
    return ''.join([
        f'_{c.lower()}' if c.isupper() else c for c in s
    ]).lstrip('_')


def pluralize(s: str) -> str:
    if s.endswith('s'):
        return s
    if s.endswith('h'):
        return s + 'es'
    if s.endswith('y'):
        return s[:-1] + 'ies'
    return s + 's'


class Base:
    @orm.declared_attr
    def __tablename__(cls: Type):
        """
        Generate table names from class names converted from CamelCase to lower
        snake_case, with an added "s" or "ies" if it end with "y"
        Examples:
        - User -> users
        - UserSetting -> user_settings
        - Country -> countries
        """
        name = cls.__name__.removesuffix('Table')
        name = camel_to_snake(name)
        name = pluralize(name)
        if hasattr(cls, '__table_prefix__'):
            name = f'{cls.__table_prefix__}_{name}'
        return name


    def __repr__(self):
        # From https://github.com/pallets/flask-sqlalchemy/blob/main/src/flask_sqlalchemy/model.py

        identity = sa.inspect(self).identity

        if identity is None:
            pk = f"(transient {id(self)})"
        else:
            pk = ", ".join(str(value) for value in identity)

        return f"<{type(self).__name__} {pk}>"
