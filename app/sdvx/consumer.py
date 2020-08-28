import os
import xml.etree.ElementTree as ET

from . import sdvx_xml
from .. import db
from .models import Apeca, Chart, Music

def import_songs_from_xml(tree):
    print('Importing songs...')
    for music_tag in tree:
        music = Music.from_xml(music_tag)
        db.session.merge(music)
        for chart_tag in music_tag.find('difficulty'):
            chart = Chart.from_xml(chart_tag, music_id=music.id)
            if chart.level != 0:
                db.session.merge(chart)
    db.session.commit()
    print('Done')

def import_apecas_from_xml(tree):
    print('Importing apecas...')
    for card_tag in tree:
        apeca = Apeca.from_xml(card_tag)
        db.session.merge(apeca)
    db.session.commit()
    print('Done')

def import_from_game_data(path):
    files = {
        '{}/others/appeal_card.xml'.format(path): import_apecas_from_xml,
        '{}/others/music_db.xml'.format(path): import_songs_from_xml,
    }
    for path, fun in files.items():
        with open(path, encoding='cp932', errors='ignore') as f:
            text = sdvx_xml.translate(f.read())
        fun(ET.fromstring(text))
    update_jacket_ids(path)

def update_jacket_ids(game_data_path, recheck=False):
    print('Updating jacket IDs...')
    for music in Music.query.all():
        folder = '{}/music/{}'.format(game_data_path, music.get_music_folder())
        # print('Working in', folder)
        for chart in Chart.query.filter_by(music_id=music.id).all():
            if not recheck and chart.jacket_id is not None:
                continue
            # print('Determining jacket_id for {} [{}]'.format(music.title, chart.diff_name))
            i = chart.difficulty
            while i > 1 and not os.path.isfile('{}/{}'.format(folder, chart.get_jacket_path(id=i))):
                i -= 1
            chart.jacket_id = i
            # print('Found file for ID', i)
    db.session.commit()
    print('Done')
