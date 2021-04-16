from app import db


class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String) # Should be unique per game!!
    name = db.Column(db.String)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    game = db.relationship('Game', backref='versions')

    @property
    def start_date(self):
        return min([x.start_date for x in self.releases if x.start_date], default=None)

    def dictify(self):
        return {
            'name': self.name,
            'releases': self.releases,
        }
