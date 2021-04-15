from .. import init_blueprint

bp = init_blueprint(__name__, prefix='/api/main')

from . import models
from .routes import game, map
