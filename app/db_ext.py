from app import db

def upsert(table, *args, **kwargs):
    commit = kwargs.pop('commit', False)
    # if filter_keys:
        # data = table.query.filter_by(**{k: kwargs[k] for k in filter_keys})
    # else:
        # data = table.query.get(*args)
    data = table.query.filter_by(**kwargs).one_or_none()
    if data is None:
        data = table(**kwargs)
        if commit:
            db.session.add(data)
            db.session.commit()
    # for k, v in kwargs.items():
    #     setattr(data, k, v)
    return data
