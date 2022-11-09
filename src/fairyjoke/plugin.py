import importlib
import inspect
import os
import time
import typing as t
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from fastapi import APIRouter, Depends

from fairyjoke import APP_PATH, Pool


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
class Plugin(Pool):
    name: str = None
    path: Path = None
    api: APIRouter = None
    frontend: APIRouter = None
    init: t.Callable = None

    @classmethod
    @property
    def current(cls) -> "Plugin":
        """Returns the plugin that is currently being executed by examining the
        Python calling stack."""

        stack = [
            Path(frame.filename)
            for frame in inspect.stack()
            if frame.filename[0] == "/"
        ]
        stack = [
            path.relative_to(APP_PATH)
            for path in stack
            if path.is_relative_to(APP_PATH)
        ]
        for plugin_path in cls.pool:
            for frame_path in stack:
                if frame_path.is_relative_to(plugin_path):
                    return cls.pool[plugin_path]
        raise ValueError("No plugin found in stack")

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

        self.pool[self.path] = self

        def _load(target, module, attr=None):
            """Loads submodule `module` to self.`target` if it is not already
            set."""
            if getattr(self, target) is not None:
                return
            setattr(self, target, _get_module(self.path, module, attr))

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
        self.init()
        delta = time.time() - now
        print(f'Finished init for "{self.name}" in {delta:.2f}s')

    @classmethod
    @property
    def data(cls):
        """Get data/ for the current plugin."""
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
