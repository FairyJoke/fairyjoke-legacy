import json
from pathlib import Path

import setuptools_scm
import toml
import yaml
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
    pool = {}

    def __init__(self, name, **kwargs):
        path = TMP_PATH / f"{name}.db"
        path.parent.mkdir(parents=True, exist_ok=True)
        super().__init__(f"sqlite:///{path}", **kwargs)

    @classmethod
    def get(cls, name):
        if name not in cls.pool:
            cls.pool[name] = cls(name)
        return cls.pool[name]


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
        with Plugin.use(plugin):
            plugin.load()
            yield plugin


class App(FastAPI):
    def __init__(self):
        super().__init__(title=APP_NAME, version=__version__)
        self.core_plugins = list(get_plugins(FAIRYJOKE_PATH / "plugins"))
        self.external_plugins = list(get_plugins(APP_PATH / "plugins"))
        self.plugins = [
            *self.core_plugins,
            *self.external_plugins,
        ]
        for plugin in self.plugins:
            with Plugin.use(plugin):
                self.mount(plugin)

        self.middleware("http")(self._unload_current_plugin)

    async def _unload_current_plugin(self, request, call_next):
        """Unloads the current plugin after the request is handled."""
        response = await call_next(request)
        Plugin.current = None
        return response

    def _init(self):
        # TODO parallelize init, may need dependency resolution for prioritization
        for plugin in self.plugins:
            plugin.run_init()

    @classmethod
    def init(cls):
        cls()._init()

    def mount(self, plugin: Plugin, tags=None) -> None:
        """Mounts the api and frontend routers of a plugin to a FastAPI app if
        they exist."""
        tags = tags or []
        if plugin.api:
            self.include_router(
                plugin.api, prefix=f"/api/{plugin.name}", tags=["API", *tags]
            )
        if plugin.frontend:
            self.include_router(
                plugin.frontend, prefix=f"/{plugin.name}", tags=["Front", *tags]
            )


class Data:
    def __init__(self, path=None):
        self.path = DATA_PATH
        if path:
            self.path = self.path / path

    def dict(self):
        for path in self.path.glob("*"):
            try:
                yield path.stem, self.load(path)
            except ValueError:
                continue

    def load(self, path):
        if path.suffix == ".json":
            return json.loads(path.read_text())
        elif path.suffix in [".yaml", ".yml"]:
            return yaml.safe_load(path.read_text())
        elif path.suffix == ".toml":
            return toml.loads(path.read_text())
        else:
            raise ValueError(f"Unknown file type: {path}")
