from flask import current_app, url_for

from app import db, xml_utils

difficulty_repr = {
    1: 'NOVICE',
    2: 'ADVANCED',
    3: 'EXHAUST',
    4: 'INFINITE',
    5: 'MAXIMUM',
}

difficulty_as_int = {v: k for k, v in difficulty_repr.items()}

difficulty_short_repr = {
    'NOVICE': 'NOV',
    'ADVANCED': 'ADV',
    'EXHAUST': 'EXH',
    'MAXIMUM': 'MXM',
    'INFINITE': 'INF',
    'GRAVITY': 'GRV',
    'HEAVENLY': 'HVN',
    'VIVID': 'VVD',
}

extra_diff_type_repr = {
    2: 'INFINITE',
    3: 'GRAVITY',
    4: 'HEAVENLY',
    5: 'VIVID',
}


class Chart(db.Model):
    __tablename__ = 'sdvx_chart'

    INFO_MAPPING = {
        'difficulty': lambda x: difficulty_as_int.get(x.tag.upper()),
        'level': {'key': 'difnum', 'fun': int},
        'illustrator': None,
        'effected_by': None,
        'limited': {'fun': int},
    }

    music_id = db.Column(db.Integer, db.ForeignKey('sdvx_music.id'), primary_key=True)
    difficulty = db.Column(db.Integer, primary_key=True) # integer representation of the difficulty name, novice = 0, advanced = 1, exhaust = 2, infinite = 3, maximum = 4
    jacket_id = db.Column(db.Integer) # internal, does not exist in SDVX, tell which difficulty to use to resolve jacket name
    level = db.Column(db.Integer)
    illustrator = db.Column(db.String)
    effected_by = db.Column(db.String)
    limited = db.Column(db.Integer)

    @classmethod
    def empty(cls, id=0):
        from . import Music
        result = cls()
        result.music = Music.empty()
        result.music_id = 0
        result.jacket_id = 0
        for key in cls.INFO_MAPPING:
            setattr(result, key, 0)
        result.difficulty = id
        result.illustrator = '???'
        result.effected_by = '???'
        return result

    @classmethod
    def from_xml(cls, xml, music_id=None):
        result = cls()
        result.music_id = music_id
        xml_utils.extractor(xml, cls.INFO_MAPPING, result)
        return result

    @property
    def diff_name(self):
        if self.difficulty == difficulty_as_int['INFINITE']:
            return extra_diff_type_repr.get(self.music.extra_diff_type)
        return difficulty_repr.get(self.difficulty)

    @property
    def diff_short(self):
        return difficulty_short_repr.get(self.diff_name)

    @property
    def jacket_small_url(self):
        return current_app.config.get('PUBLIC_URI') + url_for(
            '.get_jacket_pic',
            music_id=self.music_id, jacket_id=self.jacket_id, size='small'
        )

    @property
    def jacket_medium_url(self):
        return current_app.config.get('PUBLIC_URI') + url_for(
            '.get_jacket_pic',
            music_id=self.music_id, jacket_id=self.jacket_id, size='medium'
        )

    @property
    def jacket_large_url(self):
        return current_app.config.get('PUBLIC_URI') + url_for(
            '.get_jacket_pic',
            music_id=self.music_id, jacket_id=self.jacket_id, size='large'
        )

    def get_jacket_path(self, id=None):
        music_id = str(self.music_id).zfill(4)
        id = id or self.jacked_id
        return f'jk_{music_id}_{id}.png'
