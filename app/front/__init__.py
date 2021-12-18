from pathlib import Path
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import Router, app

MODULE_DIR = Path(__file__).parent
TEMPLATES_DIR = MODULE_DIR / 'templates'

class Jinja2Templates(Jinja2Templates):
    def __init__(self, path: Path):
        super().__init__(directory=str(path))

    def render(self, name: str, request: Request, **kwargs):
        return self.TemplateResponse(name, {'request': request} | kwargs)

templates = Jinja2Templates(TEMPLATES_DIR)
router = Router(__name__, prefix=None)
app.mount('/static', StaticFiles(directory=MODULE_DIR / 'static'), 'static')


@router.get('/')
async def index(req: Request):
    return templates.render('index.html', req)

from .routes import sdvx
router.include_router(sdvx.router)
