from .. import init_blueprint

bp = init_blueprint(__name__, prefix='/api/sdvx')

from . import api, cli, models
