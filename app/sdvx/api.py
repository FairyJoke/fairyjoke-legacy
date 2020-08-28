from flask import current_app, send_file

from . import bp
from .models import Apeca, Chart, Music

@bp.route('/api/sdvx/songs/<int:id>')
def get_music(id):
    return Music.query.get_or_404(id).as_dict()

@bp.route('/api/sdvx/songs/<int:music_id>/jacket/<size>/<int:jacket_id>.png')
@bp.route('/api/sdvx/songs/<int:music_id>/jacket/<int:jacket_id>.png')
def get_jacket(music_id, jacket_id, size='medium'):
    size_repr = {
        'small': '_s',
        'medium': '',
        'large': '_b',
    }
    if size not in size_repr:
        return 'Asked for an invalid size', 400
    music = Music.query.get_or_404(music_id)
    path = '{}/music/{}/jk_{}_{}{}.png'.format(
        current_app.config['SDVX_PATH'],
        music.get_music_folder(),
        str(music_id).zfill(4),
        jacket_id,
        size_repr[size]
    )
    try:
        return send_file(path, mimetype='image/png')
    except FileNotFoundError:
        return 'File not found', 404

@bp.route('/api/sdvx/apecas/<int:id>')
def get_apeca(id):
    return Apeca.query.get_or_404(id).as_dict()

@bp.route('/api/sdvx/apecas/<int:id>.png')
def get_apeca_pic(id):
    apeca = Apeca.query.get_or_404(id)
    path = '{}/graphics/ap_card/{}.png'.format(
        current_app.config['SDVX_PATH'],
        apeca.texture
    )
    try:
        return send_file(path, mimetype='image/png')
    except FileNotFoundError:
        return 'File not found', 404

