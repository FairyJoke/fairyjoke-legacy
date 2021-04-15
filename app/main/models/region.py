from app import db


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, unique=True)
    name = db.Column(db.String)

    def dictify(self):
        return {
            'name': self.name,
        }
