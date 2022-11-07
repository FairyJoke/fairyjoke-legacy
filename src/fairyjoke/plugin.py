import importlib
import os
import typing as t
from dataclasses import dataclass
from pathlib import Path

from fastapi import APIRouter

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

        _load("api", "api", "router")
        _load("frontend", "frontend", "router")
        _load("init", "import", "main")
        _get_module(self.path, "models")
