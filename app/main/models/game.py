from app import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    group_id = db.Column(db.Integer, db.ForeignKey('game_group.id'))
    group = db.relationship('GameGroup', backref='releases')
    key = db.Column(db.String, unique=True)
    name = db.Column(db.String)

    @property
    def start_date(self):
        return min([x.start_date for x in self.versions if x.start_date], default=None)

    @property
    def versions_count(self):
        from . import Version
        return Version.query.filter_by(game=self).count()

    @property
    def versions_query_per_platform(self):
        from sqlalchemy.sql.expression import Exists
        from . import Release, Version, Platform

        def get_platform_query(platform):
            result = Version.releases.any(Release.platform == platform)
            # also match versions without any releases as arcade releases
            if platform.name == 'arcade':
                result = result | (Version.releases == None)
            return result

        platforms = Platform.get_top_levels()
        return {
            x.name: (
                Version.query.filter(
                    Version.game == self,
                    get_platform_query(x),
                )
            )
            for x in platforms
        }

    @property
    def versions_count_per_platform(self):
        return {
            k: v.count()
            for k, v in self.versions_query_per_platform.items()
        }

    def dictify(self, with_versions=False):
        result = {
            'name': self.name,
            'group': self.group.name if self.group_id else None,
            'start_date': self.start_date,
            'versions_count': self.versions_count,
            'versions_count_per_platform': self.versions_count_per_platform,
            'active': self.active,
        }
        if with_versions:
            result['versions'] = {x.key: x for x in self.versions},
        return result
