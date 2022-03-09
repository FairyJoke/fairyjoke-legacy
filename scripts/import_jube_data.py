#!/usr/bin/env python3
import codecs
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

sys.path.append(str(Path('.').resolve()))

from app import db
from app.models import Series, Game, Version, ImportBatch

target = Path(sys.argv[1])


def hex(s: str):
    return codecs.decode(s, 'hex').decode('shift-jis')


def get(node: ET.Element, key: str, coerce=str):
    result = node.find(key)
    if result is None:
        return None
    return coerce(result.text.strip())

def bpmify(x: str):
    result = float(x)
    if result < 0:
        return None
    return result


def parse_music_db(tree, batch, clean=False):
    for tag in tree.find('body'):
        result = dict(
            id=get(tag, 'music_id', int),
            # version=get(tag, 'version', hex),
            bpm_max=get(tag, 'bpm_max', bpmify),
            bpm_min=get(tag, 'bpm_min', bpmify),
            name_string=get(tag, 'name_string', hex),
            genre=next(x.tag for x in tag.find('genre') if int(x.text)),
        )
        print(result)


if __name__ == '__main__':
    text = target.read_text(encoding='shift-jis', errors='ignore')
    tree = ET.fromstring(text)
    fun = {
        'music_info': parse_music_db,
    }.get(target.stem)
    if not fun:
        raise Exception('Unsupported')

    game_name = sys.argv[2]
    for folder in target.parents:
        if folder.stem.startswith('L44-'):
            datecode = folder.stem
            break
    else:
        datecode = sys.argv[3]
    series = db.create(Series, short='jube')
    version = db.create(Version, name=datecode, game=db.create(Game, short=game_name, series=series))
    batch = db.add(ImportBatch, version=version, commit=False)
    fun(tree, batch, clean=True)
    db.session.commit()
