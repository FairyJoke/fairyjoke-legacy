from pathlib import Path
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel as Schema


class Router(APIRouter):
    def __init__(self, module: str, prefix=True):
        module = module.removeprefix(__name__).removeprefix('.')
        self.short_prefix = module.split('.')[-1]
        if prefix is True:
            prefix = '/' + self.short_prefix
        elif not prefix:
            prefix = ''
        super().__init__(prefix=prefix)


APP_DIR = Path(__file__).parent

app = FastAPI()

from app import api, front

app.include_router(api.router)
app.include_router(front.router)
