from flask import jsonify

from .. import bp
from ..models import Game

@bp.route('/games')
def games():
    return {x.key: x for x in Game.query.all()}
