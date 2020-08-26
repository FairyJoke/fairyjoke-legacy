from flask import current_app, send_file

from . import bp
from .models import Music, Chart

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
    path = '{}/music/{}/jk_{}_{}{}.png'.format(
        current_app.config['SDVX_PATH'],
        Music.query.get_or_404(music_id).get_music_folder(),
        str(music_id).zfill(4),
        jacket_id,
        size_repr[size]
    )
    try:
        return send_file(path, mimetype='image/png')
    except FileNotFoundError:
        return 'File not found', 404
