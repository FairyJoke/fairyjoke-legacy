from fastapi import FastAPI

from fairyjoke import APP_NAME, APP_PATH, FAIRYJOKE_PATH, Plugin, __version__


class App(FastAPI):
    def __init__(self):
        super().__init__(title=APP_NAME, version=__version__)
        self.core_plugins = list(Plugin.iter(FAIRYJOKE_PATH / "plugins"))
        self.external_plugins = list(Plugin.iter(APP_PATH / "plugins"))
        self.plugins = [
            *self.core_plugins,
            *self.external_plugins,
        ]
        for plugin in self.plugins:
            self.mount(plugin)

    def _foreach_plugin(self, func):
        # TODO: Run in parallel
        for plugin in self.plugins:
            func(plugin)

    @classmethod
    def init(cls):
        cls()._foreach_plugin(Plugin.run_init)

    @classmethod
    def prepare(cls):
        cls()._foreach_plugin(Plugin.run_prepare)

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
