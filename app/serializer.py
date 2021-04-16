def dictify(obj, members):
    result = {}
    for member in members:
        value = getattr(obj, member)
        if callable(value):
            value = value(obj)
        result[member] = value
    return result

