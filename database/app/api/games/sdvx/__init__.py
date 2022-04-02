import os
from pathlib import Path
from app import Router, config


router = Router(__name__)

DATA_PATH = Path(os.environ.get('SDVX_DATA', ''))
STATIC_DATA_PATH = config.DATA_PATH / 'sdvx'

from . import models, routes
