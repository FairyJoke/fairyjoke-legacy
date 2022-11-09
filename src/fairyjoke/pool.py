class Pool:
    __AUTO_SET__ = False
    __ERROR_ON_MISSING__ = False
    pool = {}

    def _create(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get(cls, key):
        if cls.__AUTO_SET__:
            if key not in cls.pool:
                cls.pool[key] = cls._create(key=key)
        if cls.__ERROR_ON_MISSING__:
            return cls.pool[key]
        return cls.pool.get(key)
