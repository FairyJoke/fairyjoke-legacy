class Pool:
    __AUTO_SET__ = True
    __ERROR_ON_MISSING__ = False
    pool = {}

    def _create(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def _pool_pre_get(cls, key):
        return key

    @classmethod
    def get(cls, key):
        key = cls._pool_pre_get(key)
        if cls.__AUTO_SET__:
            if key not in cls.pool:
                cls.pool[key] = cls._pool_create(key=key)
        if cls.__ERROR_ON_MISSING__:
            return cls.pool[key]
        return cls.pool.get(key)
