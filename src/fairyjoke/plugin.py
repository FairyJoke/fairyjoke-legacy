import importlib
import os
import time
import typing as t
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from fastapi import APIRouter, Depends

from fairyjoke import APP_PATH


def _get_module(path, submodule=None, attr=None):
    if isinstance(path, Path):
        path = str(path)
    module_str = ".".join(path.split(os.sep))
    if submodule:
        module_str += "." + submodule
    try:
        module = importlib.import_module(module_str)
    except ModuleNotFoundError:
        return None
    if attr:
        return getattr(module, attr)
    return module


@dataclass
class Plugin:
    name: str = None
    path: Path = None
    api: APIRouter = None
    frontend: APIRouter = None
    init: t.Callable = None
    current: "Plugin" = None

    @classmethod
    @contextmanager
    def use(cls, plugin=None):
        """A context manager that sets the current plugin to `plugin`.

        ```
        with Plugin.use(plugin):
            # do stuff
        ```
        TODO: register this to be called in each route of the plugin's routers
        """
        cls.current = plugin
        yield
        cls.current = None

    @classmethod
    def from_path(cls, path):
        """Load a plugin from a path.

        The path can be either absolute or relative to the src folder.
        If a plugin is defined at that path, it will be loaded and returned,
        otherwise a new plugin will be created at that path and returned.
        """
        path = Path(path)
        if not path.is_absolute():
            path = APP_PATH / path
        path = path.relative_to(APP_PATH)
        if (path / "__init__.py").exists():
            module = _get_module(path)
            if hasattr(module, "plugin"):
                plugin = module.plugin
                plugin.path = path
                return plugin
        return cls(path=path)

    def load(self):
        """Load the plugin."""
        if self.path is None:
            raise ValueError("Plugin path is not set")
        self.path = Path(self.path)
        if not self.name:
            self.name = self.path.parts[-1]

        def _load(target, module, attr=None):
            """Loads submodule `module` to self.`target` if it is not already
            set."""
            if getattr(self, target) is not None:
                return
            setattr(self, target, _get_module(self.path, module, attr))

        with self.use(self):
            _load("api", "api", "router")
            _load("frontend", "frontend", "router")
            _load("init", "init", "main")
            _get_module(self.path, "models")

    def run_init(self):
        """Run the plugin's init function."""
        if not self.init:
            return
        print(f'Running init for "{self.name}"')
        now = time.time()
        with self.use(self):
            self.init()
        delta = time.time() - now
        print(f'Finished init for "{self.name}" in {delta:.2f}s')

    @classmethod
    @property
    def data(cls):
        from fairyjoke import Data

        return Data(cls.current.name)

    @classmethod
    @property
    def db(cls):
        from fairyjoke import Database

        return Database.get(cls.current.name)

    class Router(APIRouter):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.plugin = Plugin.current
            self.dependencies.append(Depends(self._set_current))

        def _set_current(self):
            Plugin.current = self.plugin
