import os
from pathlib import Path

from app import Router


router = Router(__name__)

DATA_JACKETS = Path(os.environ.get('DDR_JACKETS', ''))

from . import models, routes
