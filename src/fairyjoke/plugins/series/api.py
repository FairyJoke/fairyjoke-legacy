from fairyjoke import Database, Plugin
from fairyjoke.plugins.series import models

router = Plugin.Router()


@router.get("/")
def get_series():
    return router.plugin.db.session.query(models.Series).all()


@router.get("/{series_id}")
def get_series(series_id: str):
    return Database.get("series").session.query(models.Series).get(series_id)


@router.get("/{series_id}/games")
def get_series_games(series_id: str):
    return (
        Database.get("series")
        .session.query(models.SeriesGame)
        .filter(models.SeriesGame.series_id == series_id)
        .all()
    )


@router.get("/{series_id}/games/{game_id}")
def get_series_game(series_id: str, game_id: str):
    return (
        Database.get("series")
        .session.query(models.SeriesGame)
        .filter(models.SeriesGame.series_id == series_id)
        .filter(models.SeriesGame.id == game_id)
        .one()
    )
