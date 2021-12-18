from typing import Type
from sqlalchemy import orm


def camel_to_snake(s: str) -> str:
    return ''.join([
        f'_{c.lower()}' if c.isupper() else c for c in s
    ]).lstrip('_')


def pluralize(s: str) -> str:
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
        name = camel_to_snake(cls.__name__)
        name = pluralize(name)
        if hasattr(cls, '__table_prefix__'):
            name = f'{cls.__table_prefix__}_{name}'
        return name
