from fairyjoke import Plugin
from fairyjoke.plugins.series import models


def main():
    Plugin.db.init()
    groups = {}
    for series_id, series_data in Plugin.data.dict():
        group = series_data.get("group")
        if group:
            if group not in groups:
                obj = models.SeriesGroup(id=group, name=group)
                groups[group] = obj
                Plugin.db.session.add(obj)
            group = groups[group]

        series = models.Series(
            id=series_id,
            name=series_data["name"],
            active=series_data.get("active", True),
            translation=series_data.get("translation"),
            group=group,
        )
        Plugin.db.session.add(series)

        for game_id, game_data in series_data.get("games", {}).items():
            game = models.SeriesGame(
                id=game_id,
                name=game_data["name"],
                series=series,
                date=game_data.get("date"),
            )
            Plugin.db.session.add(game)
    Plugin.db.session.commit()
