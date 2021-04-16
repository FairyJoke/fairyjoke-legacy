from flask import current_app, jsonify, request, send_file

from app import is_strict
from .. import bp
from ..models import Chart, Music

@bp.route('/songs')
def search_music():
    omni = request.args.get('omni')
    search_fields = {
        'title': Music,
        'artist': Music,
        'illustrator': Chart,
        'effected_by': Chart,
    }
    level = request.args.get('level')
    genre = request.args.get('genre')
    query = Chart.query.join(Music).with_entities(Chart.music_id)
    for key, table in search_fields.items():
        value = request.args.get(key)
        if not value:
            continue
        query = query.filter(getattr(table, key).ilike('%{}%'.format(value)))
    if level:
        query = query.filter(Chart.level == int(level))
    if genre:
        genre = int(genre)
        if genre == 0:
            query = query.filter(Music.genre_id == genre)
        else:
            query = query.filter(Music.genre_id.op('&')(genre))
    if omni:
        query = query.filter(
            Music.title.ilike('%{}%'.format(omni))
            | Music.artist.ilike('%{}%'.format(omni))
            | Music.ascii.ilike('%{}%'.format(omni))
            | Chart.illustrator.ilike('%{}%'.format(omni))
            | Chart.effected_by.ilike('%{}%'.format(omni))
        )
    results = [x[0] for x in query.group_by(Chart.music_id).paginate(
        int(request.args.get('page', 1)),
        current_app.config.get('PER_PAGE'),
        False
    ).items]
    return jsonify([x.as_dict() for x in Music.query.filter(Music.id.in_(results)).all()])


@bp.route('/songs/<int:id>')
def get_music(id):
    result =  Music.query.get(id)
    if not result:
        if is_strict():
            return 'Song not found', 404
        result = Music.empty()
    result = result.as_dict()
    return result

@bp.route('/songs/<int:music_id>/jacket/<size>/<int:jacket_id>.png')
@bp.route('/songs/<int:music_id>/jacket/<int:jacket_id>.png')
def get_jacket_pic(music_id, jacket_id, size='medium'):
    size_repr = {
        'small': '_s',
        'medium': '',
        'large': '_b',
    }
    if size not in size_repr:
        return 'Asked for an invalid size', 400
    music = Music.query.get(music_id)
    if not music:
        if is_strict():
            return 'Song not found', 404
    dummy_path = '{}/graphics/jk_dummy{}.png'.format(
        current_app.config['SDVX_PATH'],
        size_repr[size],
    )
    path = '{}/music/{}/jk_{}_{}{}.png'.format(
        current_app.config['SDVX_PATH'],
        music.get_music_folder(),
        str(music_id).zfill(4),
        jacket_id,
        size_repr[size]
    ) if music else dummy_path
    try:
        return send_file(path, mimetype='image/png')
    except FileNotFoundError:
        if not is_strict():
            return send_file(dummy_path, mimetype='image/png')
        return 'File not found', 404
