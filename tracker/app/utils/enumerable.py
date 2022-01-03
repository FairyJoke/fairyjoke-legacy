class Enumerable:
    @classmethod
    def keys(cls):
        return [x for x in cls.__dict__.keys() if not x.startswith('_')]
