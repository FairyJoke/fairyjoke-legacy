from .. import init_blueprint

bp = init_blueprint(__name__)

from . import models, routes
