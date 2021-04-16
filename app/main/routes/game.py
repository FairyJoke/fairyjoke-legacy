from .. import bp
from ..models import Game

@bp.route('/games')
def games():
    return {
        x.key: x.dictify()
        for x in Game.query.all()
    }

@bp.route('/games/<string:key>')
def game(key):
    result = Game.query.filter_by(key=key).first_or_404()
    return result.dictify()
