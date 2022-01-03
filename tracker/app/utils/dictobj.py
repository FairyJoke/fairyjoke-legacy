class DictObj(dict):
    class UNSET:
        pass

    class Meta:
        defaults = {}

        @classmethod
        def has_default(cls, d):
            return id(d) in cls.defaults

        @classmethod
        def default(cls, d):
            return cls.defaults[id(d)]


    def __init__(self, *args, default=UNSET, **kwargs):
        if default != self.UNSET:
            self.Meta.defaults[id(self)] = default
        super().__init__()
        for arg in args:
            try:
                kwargs |= dict(arg)
            except TypeError:
                pass
        if kwargs:
            super().__init__(**kwargs)

    def __getattr__(self, name):
        if name in self.keys():
            return self[name]
        if self.Meta.has_default(self):
            return self.Meta.default(self)
        raise AttributeError(f'Object {self} has no attribute {name}')

    def __setattr__(self, name, value):
        self[name] = value
