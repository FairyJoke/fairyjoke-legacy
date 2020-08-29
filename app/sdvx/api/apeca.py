from flask import current_app, send_file

from .. import bp
from ..models import Apeca

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
