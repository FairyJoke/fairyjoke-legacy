import xml.etree.ElementTree as ET

from .. import db
from .models import Music, Chart

def import_from_xml(tree):
    for music_tag in tree:
        music = Music.from_xml(music_tag)
        db.session.merge(music)
        for chart_tag in music_tag.find('difficulty'):
            chart = Chart.from_xml(chart_tag, music_id=music.id)
            if chart.level is not 0:
                db.session.merge(chart)
    db.session.commit()

def import_from_game_data(path):
    with open('{}/others/music_db.xml'.format(path), encoding='shift_jisx0213') as f:
        music_db_txt = f.read()
    import_from_xml(ET.fromstring(music_db_txt))
