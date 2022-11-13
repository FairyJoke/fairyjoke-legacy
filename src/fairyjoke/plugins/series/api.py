from fairyjoke import Plugin

from .models import Series, SeriesGame

router = Plugin.Router()


@router.get("/")
def get_series(group: str = None):
    query = Plugin.db.session.query(Series)
    query = query.match(group_id=group)
    return query.all()


@router.get("/{series_id}")
def get_series(series_id: str):
    return Plugin.db.session.query(Series).get(series_id)


@router.get("/{series_id}/games")
def get_series_games(series_id: str):
    return Plugin.db.session.query(SeriesGame).match(series_id=series_id).all()


@router.get("/{series_id}/games/{game_id}")
def get_series_game(series_id: str, game_id: str):
    return (
        Plugin.db.session.query(SeriesGame)
        .match(series_id=series_id, id=game_id)
        .one()
    )
