from typing import Type

from . import session


def add(table, keys=None, commit=True, **extra_keys):
    keys = keys or {}
    keys |= extra_keys
    result = table(**keys)
    session.add(result)
    print('ADD', result) #TODO use stdlib logging
    if commit:
        session.commit()
    return result


def create(
    table: Type,
    search_keys: dict = None,
    create_keys=None,
    commit=True,
    include_search_in_create=True,
    update=False,
    **extra_search_keys,
) -> object:
    search_keys = search_keys or {}
    search_keys |= extra_search_keys
    result = session.query(table).filter_by(**search_keys).first()
    if not result:
        create_keys = create_keys or {}
        if include_search_in_create:
            create_keys = search_keys | create_keys
        result = add(table, create_keys, commit=commit)
    elif update:
        for key, value in create_keys.items():
            setattr(result, key, value)
        if commit:
            session.commit()
    return result
