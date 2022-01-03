from fastapi import FastAPI, APIRouter


class Router(APIRouter):
    def __init__(self, module: str, prefix=True):
        module = module.removeprefix(__name__).removeprefix('.')
        self.short_prefix = module.split('.')[-1]
        if prefix is True:
            prefix = '/' + self.short_prefix
        elif not prefix:
            prefix = ''
        super().__init__(prefix=prefix)


app = FastAPI()

from app import models, routes
