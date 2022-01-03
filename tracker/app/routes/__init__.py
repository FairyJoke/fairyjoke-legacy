import importlib
from pathlib import Path

from app import app


CURRENT_MODULE = __name__

for path in Path(__file__).parent.glob('./*.py'):
    if path.stem == '__init__':
        continue
    module = importlib.import_module(f'.{path.stem}', CURRENT_MODULE)
    if hasattr(app, 'router'):
        app.include_router(module.router)
