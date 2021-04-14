from flask import current_app, url_for

from app import db, serializer, xml_utils


class Apeca(db.Model):
    __tablename__ = 'sdvx_apeca'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    texture = db.Column(db.String)
    illustrator = db.Column(db.String)
    rarity = db.Column(db.Integer)
    sort_no = db.Column(db.Integer)
    genre_id = db.Column(db.Integer)
    # Skipped: messages, is_default, distribution_date (weird format, 32nd July wtf)

    @staticmethod
    def from_xml(xml):
        result = Apeca()
        result.id = int(xml.get('id'))
        info_mapping = {
            'title': None,
            'texture': None,
            'illustrator': None,
            'rarity': {'fun': int},
            'sort_no': {'fun': int},
            'genre_id': {'key': 'genre', 'fun': int},
        }
        xml_utils.extractor(xml.find('info'), info_mapping, result)
        return result

    def as_dict(self):
        return serializer.dictify(self, [
            'id', 'title', 'texture', 'illustrator', 'rarity', 'sort_no',
            'genre_id', 'url',
        ])

    @property
    def url(self):
        return current_app.config.get('PUBLIC_URI') + url_for('.get_apeca_pic', id=self.id)
