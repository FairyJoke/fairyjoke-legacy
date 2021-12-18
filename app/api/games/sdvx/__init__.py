import os
from pathlib import Path
from app import Router


router = Router(__name__)

DATA_PATH = Path(os.environ.get('SDVX_DATA', ''))

from . import models, routes
