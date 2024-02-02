from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Schema(BaseModel):
    class Config:
        from_attributes = True


class Router(APIRouter):
    def __init__(self, module: str, prefix=True):
        module = module.removeprefix(__name__).removeprefix(".")
        self.short_prefix = module.split(".")[-1]
        if prefix is True:
            prefix = "/" + self.short_prefix
        elif not prefix:
            prefix = ""
        super().__init__(prefix=prefix)


APP_DIR = Path(__file__).parent

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app import api, front

app.include_router(api.router)
app.include_router(front.router)

from app import models
