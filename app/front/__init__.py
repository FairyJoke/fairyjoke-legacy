import importlib
from pathlib import Path
import urllib.parse
import jinja2
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import Router, app

MODULE_DIR = Path(__file__).parent
TEMPLATES_DIR = MODULE_DIR / 'templates'
router = Router(__name__, prefix=None)

class Jinja2Templates(Jinja2Templates):
    def __init__(self, path: Path):
        super().__init__(directory=str(path))

        @jinja2.pass_context
        def url_for(context, name, query=None, keep_args=False, **params):
            query = query or {}
            request = context['request']
            if name:
                result = app.url_path_for(name, **params)
            else:
                result = ''
            if keep_args:
                query = dict(request.query_params) | query
            if query:
                query = urllib.parse.urlencode(query, doseq=True)
                result += '?' + query
            return result
        self.env.globals['url_for'] = url_for

    def render(self, name: str, request: Request, **kwargs):
        return self.TemplateResponse(
            name,
            {'request': request, 'template_name': name} | kwargs
        )


templates = Jinja2Templates(TEMPLATES_DIR)
app.mount('/static', StaticFiles(directory=MODULE_DIR / 'static'), 'static')

for file in Path(__file__).parent.glob('./routes/*'):
    if file.stem.startswith('_'):
        continue
    module = importlib.import_module(f'{__name__}.routes.{file.stem}')
    if hasattr(module, 'router'):
        router.include_router(module.router)


@router.get('/')
async def home():
    return RedirectResponse(router.url_path_for('games'))
