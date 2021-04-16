from pathlib import Path
import logging
import json
import yaml

from app import db, db_ext
from app.json_encoder import CustomJSONEncoder

log = logging.getLogger(__name__)

class Importer:
    FOLDER_PATH = './imports'

    @staticmethod
    def update(target, key, source, model=None, model_key=None):
        if key in source:
            data = source[key]
            log.info(f'Found {key} in {source}, updating {target}')
            if model:
                data = db_ext.upsert(
                    model,
                    **{model_key if model_key is not None else key: data}
                )
            setattr(target, key, data)
        return target

    @staticmethod
    def log(obj):
        log.info(f'Imported {obj}')

    def commit(self, obj):
        if self.dry:
            return
        db.session.add(obj)
        db.session.commit()
        log.info('Committed')

    def run(self, dry=False, dump=False):
        self.dry = dry
        folder = Path(self.FOLDER_PATH)
        datas = {}
        for file in (folder / 'games').glob('*.yaml'):
            with open(file) as f:
                datas[file.stem] = yaml.safe_load(f)
        if dump:
            print(json.dumps(datas, indent=2, cls=CustomJSONEncoder))
        for key, data in datas.items():
            try:
                game = GameImporter(dry=self.dry).run(key, data)
                self.commit(game)
            except Exception as e:
                log.error(f'Failed while importing {data}')
                log.error(e, exc_info=True)
                db.session.rollback()

    def __init__(self, dry=False):
        self.dry = dry


class VersionImporter(Importer):
    def run(self, key, data, game=None):
        from app.main.models import Version, Platform, Region, Release, ReleaseType

        result = db_ext.upsert(Version, key=key, game=game)
        self.update(result, 'name', data)
        for release in data.get('releases', []):
            platform = (
                db_ext.upsert(Platform, name=release['platform'])
                if 'platform' in release
                else None
            )
            region = (
                db_ext.upsert(Region, key=release['region'])
                if 'region' in release
                else None
            )
            type = (
                db_ext.upsert(ReleaseType, key=release['type'])
                if 'type' in release
                else None
            )
            release = db_ext.upsert(
                Release,
                version=result,
                start_date=release.get('date'),
                platform=platform,
                region=region,
                type=type,
            )
        self.log(result)
        return result


class GameImporter(Importer):
    def run(self, key, data):
        from app.main.models import Game, GameGroup

        result = db_ext.upsert(Game, key=key)
        self.commit(result)
        self.update(result, 'name', data)
        self.update(result, 'active', data)
        self.update(result, 'group', data, GameGroup, 'name')
        for ver_key, ver_data in data.get('versions', {}).items():
            VersionImporter().run(ver_key, ver_data, game=result)
        self.log(result)
        return result
