from fastapi.requests import Request

from app import Router, db
from app.models import Series
from .. import templates


router = Router(__name__)


@router.get('/')
async def games(req: Request):
    query = db.session.query(Series)
    return templates.render('games.html', req, series=query)
