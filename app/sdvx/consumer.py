import os
import xml.etree.ElementTree as ET

from .. import db
from .models import Music, Chart

def import_from_xml(tree):
    for music_tag in tree:
        music = Music.from_xml(music_tag)
        db.session.merge(music)
        for chart_tag in music_tag.find('difficulty'):
            chart = Chart.from_xml(chart_tag, music_id=music.id)
            if chart.level != 0:
                db.session.merge(chart)
    db.session.commit()

def import_from_game_data(path):
    with open('{}/others/music_db.xml'.format(path), encoding='shift_jisx0213') as f:
        music_db_txt = f.read()
    import_from_xml(ET.fromstring(music_db_txt))
    update_jacket_ids('{}/music'.format(path))

def update_jacket_ids(music_folder, recheck=False):
    print('Initiated SDVX jackets ID discovery')
    for music in Music.query.all():
        padded_id = str(music.id).zfill(4)
        folder = '{}/{}_{}'.format(music_folder, padded_id, music.ascii)
        print('Working in', folder)
        for chart in Chart.query.filter_by(music_id=music.id).all():
            if not recheck and chart.jacket_id is not None:
                continue
            print('Determining jacket_id for {} [{}]'.format(music.title, chart.diff_name))
            i = chart.difficulty + 1
            while i > 1 and not os.path.isfile('{}/jk_{}_{}.png'.format(folder, padded_id, i)):
                print('file not found')
                i -= 1
            chart.jacket_id = i
            print('Found file for ID', i)
    db.session.commit()
