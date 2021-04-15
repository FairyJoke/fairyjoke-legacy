from app import db


class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    region = db.relationship('Region', backref='releases')
    version_id = db.Column(db.Integer, db.ForeignKey('version.id'), nullable=False)
    version = db.relationship('Version', backref='releases')
    release_type_id = db.Column(db.Integer, db.ForeignKey('release_type.id'))
    release_type = db.relationship('ReleaseType', backref='releases')
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    platform = db.relationship('Platform', backref='releases')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def dictify(self):
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'platform': self.platform.name if self.platform_id else None,
            'region': self.region.name if self.region_id else None,
            'type': self.release_type.key if self.release_type_id else None,
        }
