import importlib
from pathlib import Path

from app import Router


router = Router(__name__)

PATH = Path(__file__).parent
CURRENT_MODULE = __name__

for path in PATH.glob('./*/'):
    if not path.is_dir() or path.stem == '__pycache__':
        continue
    module = importlib.import_module(f'.{path.stem}', CURRENT_MODULE)
    if hasattr(module, 'router'):
        router.include_router(module.router)


@router.get('/')
async def index():
    return 'hello games'
