from datetime import date
import logging
from flask.json import JSONEncoder

# from https://stackoverflow.com/a/43663918
class CustomJSONEncoder(JSONEncoder):
    FAILED = '__jsonify_failed'

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            if getattr(obj, 'dictify', False):
                return obj.dictify()
            # iterable = iter(obj)
            # return list(iterable)
            return JSONEncoder.default(self, obj)
        except TypeError as e:
            logging.warning(f'Ignored JSON serializing of {obj} due to {e}')
            # return None
            return self.FAILED

class Dumpable:
    def dictify(self):
        from sqlalchemy.orm.collections import InstrumentedList
        keys = getattr(self, '__schema__', [])
        print(self, '\n\n')
        if hasattr(self, '__table__'):
            for k in self.__dir__():
                print(k, type(getattr(self, k)))
            # Import columns
            keys += [c.name for c in self.__table__.columns]
            # Import backrefs
            keys += [
                k for k in self.__dir__()
                if isinstance(getattr(self, k), InstrumentedList)
            ]
        return {k: getattr(self, k) for k in keys}
