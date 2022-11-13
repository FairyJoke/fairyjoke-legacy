from pathlib import Path

import setuptools_scm

# Exposed variables

FAIRYJOKE_PATH = Path(__file__).parent
APP_PATH = FAIRYJOKE_PATH.parent
DATA_PATH = Path("data")
TMP_PATH = Path("tmp")
APP_NAME = "FairyJoke"
__version__ = setuptools_scm.get_version(
    root=APP_PATH.parent,
    local_scheme=lambda x: f"+branch={x.branch},commit={x.node}",
)

# Exposed imports
# Order matters here, if we want to be able to use direct fairyjoke imports from
# the modules defined here, we need to ensure the dependencies are imported
# before the dependent ones
# So from top to bottom, we should list the simplest ones down to the most
# complex ones

# isort: off

from fairyjoke.data import Data

from fairyjoke.database import Database as Database

from fairyjoke.plugin import Plugin as Plugin

from fairyjoke.pool import Pool as Pool

from fairyjoke.app import App
