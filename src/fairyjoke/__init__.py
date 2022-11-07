import shutil
from pathlib import Path

import setuptools_scm
from fastapi import FastAPI
from sqlalchemy_setup import Database as _Database

FAIRYJOKE_PATH = Path(__file__).parent
APP_PATH = FAIRYJOKE_PATH.parent
DATA_PATH = Path("data")
TMP_PATH = Path("tmp")
APP_NAME = "FairyJoke"
__version__ = setuptools_scm.get_version(
    root=APP_PATH.parent,
    local_scheme=lambda x: f"+branch={x.branch},commit={x.node}",
)

from fairyjoke.plugin import Plugin


class Database(_Database):
    def __init__(self, name, **kwargs):
        path = TMP_PATH / f"{name}.db"
        path.parent.mkdir(parents=True, exist_ok=True)
        super().__init__(f"sqlite:///{path}", **kwargs)


db = Database("core")


def get_plugins(path: Path) -> list[Plugin]:
    """Fetches plugins at a path.

    Assumes that every subdirectory of `path` is a plugin."""
    for path in path.glob("*/"):
        # Trailing slash to match only dirs is only available in Python 3.11+
        # https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
        # We can remove this check when we drop support for Python 3.10
        if not path.is_dir():
            continue
        plugin = Plugin.from_path(path)
        plugin.load()
        yield plugin


core_plugins = list(get_plugins(FAIRYJOKE_PATH / "plugins"))
external_plugins = list(get_plugins(APP_PATH / "plugins"))
plugins = [
    *core_plugins,
    *external_plugins,
]


def init():
    db.init()

    # TODO parallelize init, may need dependency resolution for prioritization
    for plugin in plugins:
        if plugin.init:
            plugin.init()


def create_app() -> FastAPI:
    app = FastAPI(title=__name__, version=__version__)
    for plugin in plugins:
        mount_plugin(app, plugin)
    return app


def mount_plugin(app: FastAPI, plugin: Plugin, tags=None) -> None:
    """Mounts the api and frontend routers of a plugin to a FastAPI app if they
    exist."""
    tags = tags or []
    if plugin.api:
        app.include_router(
            plugin.api, prefix=f"/api/{plugin.name}", tags=["API", *tags]
        )
    if plugin.frontend:
        app.include_router(
            plugin.frontend, prefix=f"/{plugin.name}", tags=["Front", *tags]
        )
