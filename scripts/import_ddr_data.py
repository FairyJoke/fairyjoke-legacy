#!/usr/bin/env python3
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

sys.path.append(str(Path('.').resolve()))

from app import db
from app.models import Version, ImportBatch, Series, Game
from app.api.games.ddr.models import (
    Music, Difficulty, Playstyles, Difficulties, DifficultyImport
)

target = Path(sys.argv[1])


def get(node: ET.Element, key: str, coerce=str):
    result = node.find(key)
    if result is None:
        return None
    return coerce(result.text)

def bpmify(x: str):
    return int(x)


def parse_music_db(tree, batch, clean=False):
    if clean:
        db.session.query(Difficulty).delete()
        db.session.query(Music).delete()
        db.session.commit()
    for tag in tree:
        music = db.create(
            Music,
            {'id': get(tag, 'mcode', int)},
            {
                'label':            get(tag, 'basename'),
                'title':            get(tag, 'title'),
                'title_yomigana':   get(tag, 'title_yomi'),
                'artist':           get(tag, 'artist'),
                'bpm_min':          get(tag, 'bpmmin', bpmify),
                'bpm_max':          get(tag, 'bpmmax', bpmify),
                'background_type':  get(tag, 'bgstage', int),
                'series':           get(tag, 'series', int),
            },
            commit=False,
            update=True,
        )
        diffs = tag.find('diffLv')
        for i, level in enumerate(diffs.text.split(' ')):
            level = int(level)
            if not level:
                continue
            print(level, i)
            if i <= 5:
                style = Playstyles.SP
            else:
                style = Playstyles.DP
                i -= 5
            difficulty = db.create(
                Difficulty,
                {
                    'music_id': music.id,
                    'diff': Difficulties(i),
                    'playstyle': style,
                },
                {
                    'level': level,
                },
                commit=False,
                update=True,
            )
            db.add(DifficultyImport, batch=batch, difficulty=difficulty, commit=False)


if __name__ == '__main__':
    text = target.read_text(errors='ignore')
    tree = ET.fromstring(text)
    fun = {
        'musicdb': parse_music_db,
    }.get(target.stem)
    if not fun:
        raise Exception('Unsupported')

    game_name = sys.argv[2]
    for folder in target.parents:
        if folder.stem.startswith('MDX-'):
            datecode = folder.stem
            break
    else:
        datecode = sys.argv[3]
    series = db.create(Series, short='ddr')
    version = db.create(Version, name=datecode, game=db.create(Game, short=game_name, series=series))
    batch = db.add(ImportBatch, version=version, commit=False)
    fun(tree, batch, clean=True)
    db.session.commit()
