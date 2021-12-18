from app import Router
from . import games


router = Router(__name__)

router.include_router(games.router)
