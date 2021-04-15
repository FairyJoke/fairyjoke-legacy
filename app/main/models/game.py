from app import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('game_group.id'))
    group = db.relationship('GameGroup', backref='releases')
    key = db.Column(db.String, unique=True)
    name = db.Column(db.String)

    def dictify(self):
        return {
            'name': self.name,
            'versions': {x.key: x for x in self.versions},
            'group': self.group.name if self.group_id else None,
        }
