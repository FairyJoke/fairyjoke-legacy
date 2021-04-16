from .. import bp
from ..models import Game, Version

@bp.route('/games')
def games():
    return {
        x.key: x
        for x in Game.query.all()
    }

@bp.route('/games/<string:key>')
def game(key):
    result = Game.query.filter_by(key=key).first_or_404()
    return result.dictify()

@bp.route('/games/<string:game>/<string:version>')
def game_version(game, version):
    game = Game.query.filter_by(key=game).first_or_404()
    result = Version.query.filter_by(key=version, game=game).first_or_404()
    return result.dictify()
