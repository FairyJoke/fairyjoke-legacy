from app import db


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    parent_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    parent = db.relationship('Platform')

    def dictify(self):
        return {
            'name': self.name,
            'parent': self.parent,
        }
