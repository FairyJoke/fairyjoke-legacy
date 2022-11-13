import importlib
import inspect
import os
import time
import typing as t
from dataclasses import dataclass
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from jinja2 import ChoiceLoader, Environment, PackageLoader, select_autoescape

from fairyjoke import APP_PATH
from fairyjoke.pool import Pool


def _get_module_str(path, submodule):
    if isinstance(path, Path):
        path = str(path)
    module_str = ".".join(path.split(os.sep))
    if submodule:
        module_str += "." + submodule
    return module_str


def _get_module(path, submodule=None, attr=None):
    module_str = _get_module_str(path, submodule)
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
    prepare: t.Callable = None

    templating: Environment = None

    @property
    def module_str(self) -> str:
        return str(self.path).replace(os.sep, ".")

    @property
    def relative_path(self):
        return APP_PATH / self.path

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
    def _pool_pre_get(cls, key):
        return Path(key)

    @classmethod
    def _pool_create(cls, key):
        return cls.from_path(key)

    @classmethod
    def iter(cls, path: Path) -> t.Iterator["Plugin"]:
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

        if path in cls.pool:
            return cls.get(path)

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

        if not self.templating and (self.relative_path / "templates").exists():
            self.templating = Environment(
                loader=ChoiceLoader(
                    [
                        PackageLoader(self.module_str),
                        PackageLoader("fairyjoke"),
                    ]
                ),
                autoescape=select_autoescape(),
            )

        def _load(target, module, attr=None):
            """Loads submodule `module` to self.`target` if it is not already
            set."""
            if getattr(self, target) is not None:
                return
            setattr(self, target, _get_module(self.path, module, attr))

        _load("api", "api", "router")
        _load("frontend", "frontend", "router")
        _load("init", "init", "main")
        _load("prepare", "prepare", "main")
        _get_module(self.path, "models")

    def _run_func(self, name):
        func = getattr(self, name)
        if not func:
            return
        print(f'Running {name} for "{self.name}"')
        now = time.time()
        func()
        delta = time.time() - now
        print(f'Finished running {name} for "{self.name}" in {delta:.2f}s')

    def run_init(self):
        """Run the plugin's init function."""
        self._run_func("init")

    def run_prepare(self):
        """Run the plugin's prepare function."""
        self._run_func("prepare")

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

        def template(self, template="index.html", context={}, **kwargs):
            context |= kwargs
            return self.plugin.templating.get_template(template).render(
                **context
            )

        def html(self, *args, **kwargs):
            kwargs.setdefault("response_class", HTMLResponse)
            return self.get(*args, **kwargs)
