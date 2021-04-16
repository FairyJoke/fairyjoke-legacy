from app import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    group_id = db.Column(db.Integer, db.ForeignKey('game_group.id'))
    group = db.relationship('GameGroup', backref='releases')
    key = db.Column(db.String, unique=True)
    name = db.Column(db.String)

    def dictify(self, with_versions=False):
        result = {
            'name': self.name,
            'group': self.group.name if self.group_id else None,
        }
        if with_versions:
            result['versions'] = {x.key: x for x in self.versions},
        return result
