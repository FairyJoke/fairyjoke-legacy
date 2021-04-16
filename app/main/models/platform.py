from app import db


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    parent_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    parent = db.relationship('Platform', uselist=False, foreign_keys=[parent_id], remote_side=[id], backref='children')

    @classmethod
    def get_top_levels(cls):
        return cls.query.filter(Platform.parent == None).all()

    def dictify(self):
        return {
            'name': self.name,
            'parent': self.parent,
        }
