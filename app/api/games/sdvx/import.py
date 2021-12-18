from datetime import date
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from app import db
from app.api.games.sdvx.models import Apeca, Music, Difficulty, Difficulties

target = Path(sys.argv[1])
MUSIC_FOLDER = target.parent / '..' / 'music'
if not MUSIC_FOLDER.exists():
    print('music folder not found')
    MUSIC_FOLDER = False


def get(node: ET.Element, key: str, coerce=str):
    return coerce(
        node.get(key)
        or node.find(key).text
    )


TRANSLATION_TABLE = str.maketrans(
    '曦曩齷罇驩驫騫齲齶骭龕黻齲齪',
    'àèéêØāá♥♡ü€*♥♣'
)


def translate(x: str):
    return x.translate(TRANSLATION_TABLE)


def bpmify(x: str):
    return int(x) / 100


def dateify(x: str):
    return date.fromisoformat(f'{x[0:4]}-{x[4:6]}-{x[6:8]}')


def diffify(x: str):
    return {
        '2': Difficulties.INF,
        '3': Difficulties.GRV,
        '4': Difficulties.HVN,
        '5': Difficulties.VVD,
    }.get(x)

def parse_music_db(tree):
    for tag in tree:
        info: ET.Element = tag.find('info')
        music_id = get(tag, 'id', int)
        music = db.create(
            Music,
            {'id': music_id},
            {
                'label':            get(info, 'label'),
                'title':            get(info, 'title_name'),
                'title_yomigana':   get(info, 'title_yomigana'),
                'artist':           get(info, 'artist_name'),
                'artist_yomigana':  get(info, 'artist_yomigana'),
                'ascii':            get(info, 'ascii'),
                'bpm_min':          get(info, 'bpm_min', bpmify),
                'bpm_max':          get(info, 'bpm_max', bpmify),
                'release_date':     get(info, 'distribution_date', dateify),
                'background_type':  get(info, 'bg_no', int),
                'genre':            get(info, 'genre', int),
                'extra_difficulty': get(info, 'inf_ver', diffify),
            },
            commit=False,
            update=True,
        )
        diffs = tag.find('difficulty')
        jacket_id = 1
        for diff in diffs:
            level = get(diff, 'difnum', int)
            if not level:
                continue
            difficulty = db.create(
                Difficulty,
                {
                    'music_id': music_id,
                    'name':
                        Difficulties(diff.tag.upper())
                        if diff.tag != 'infinite'
                        else music.extra_difficulty
                    ,
                },
                {
                    'level': level,
                    'illustrator': get(diff, 'illustrator'),
                    'effector': get(diff, 'effected_by'),
                },
                commit=False,
                update=True,
            )
            if MUSIC_FOLDER:
                folder = MUSIC_FOLDER / music.folder
                this_jacket = int(difficulty.name)
                if (folder / difficulty.get_filename(jacket_id=this_jacket)).exists():
                    jacket_id = this_jacket
                difficulty.jacket_id = jacket_id


def parse_apecas(tree):
    for tag in tree:
        info: ET.Element = tag.find('info')
        card_id = get(tag, 'id', int)
        db.create(
            Apeca,
            {'id': card_id},
            {
                'title': get(info, 'title'),
                'texture': get(info, 'texture'),
                'illustrator': get(info, 'illustrator'),
                'rarity': get(info, 'rarity', int),
                'sort': get(info, 'sort_no', int),
                'generator': get(info, 'generator_no', int),
                'genre': get(info, 'genre', int),
                'messages': {
                    c: get(info, f'message_{c}')
                    for c in 'abcdefgh'
                },
            },
            commit=False,
            update=True,
        )


if __name__ == '__main__':
    text = target.read_text(encoding='cp932', errors='ignore')
    text = translate(text)
    tree = ET.fromstring(text)
    fun = {
        'music_db': parse_music_db,
        'appeal_card': parse_apecas,
    }.get(target.stem)
    if not fun:
        raise Exception('Unsupported')
    fun(tree)
    db.session.commit()
