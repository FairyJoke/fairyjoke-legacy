from .. import db, xml_utils
from . import sdvx_xml

difficulty_repr = {
    0: 'NOVICE',
    1: 'ADVANCED',
    2: 'EXHAUST',
    3: 'INFINITE',
    4: 'MAXIMUM',
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

class Music(db.Model):
    __tablename__ = 'sdvx_music'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    title = db.Column(db.String)
    title_yomigana = db.Column(db.String)
    artist = db.Column(db.String)
    artist_yomigana = db.Column(db.String)
    ascii = db.Column(db.String)
    bpm_max = db.Column(db.Float)
    bpm_min = db.Column(db.Float)
    release_date = db.Column(db.Date)
    background_id = db.Column(db.Integer) # not sure, known as bg_no
    genre_id = db.Column(db.Integer)
    version = db.Column(db.Integer)
    demo_pri = db.Column(db.Integer) # ?
    extra_diff_type = db.Column(db.Integer) # 0 = None, 2 = INF, 3 = GRV, 4 = HVN, 5 = VVD
    # Skipped: volume (all 91s), is_fixed (all 1s)

    @staticmethod
    def from_xml(xml):
        result = Music()
        result.id = xml.get('id')
        info_mapping = {
            'label': None,
            'title': 'title_name',
            'title_yomigana': None,
            'artist': 'artist_name',
            'artist_yomigana': None,
            'ascii': None,
            'bpm_max': {'fun': sdvx_xml.bpmify},
            'bpm_min': {'fun': sdvx_xml.bpmify},
            'release_date': {'key': 'distribution_date', 'fun': sdvx_xml.dateify},
            'background_id': {'key': 'bg_no', 'fun': int},
            'genre_id': {'key': 'genre', 'fun': int},
            'version': {'fun': int},
            'demo_pri': {'fun': int},
            'extra_diff_type': {'key': 'inf_ver', 'fun': int},
        }
        xml_utils.extractor(xml.find('info'), info_mapping, result)
        return result

class Chart(db.Model):
    __tablename__ = 'sdvx_chart'

    music_id = db.Column(db.Integer, db.ForeignKey('sdvx_music.id'), primary_key=True)
    difficulty = db.Column(db.Integer, primary_key=True) # integer representation of the difficulty name, novice = 0, advanced = 1, exhaust = 2, infinite = 3, maximum = 4
    jacket_id = db.Column(db.Integer) # internal, does not exist in SDVX, tell which difficulty to use to resolve jacket name
    level = db.Column(db.Integer)
    illustrator = db.Column(db.String)
    effected_by = db.Column(db.String)
    limited = db.Column(db.Integer)

    @staticmethod
    def from_xml(xml, music_id=None):
        result = Chart()
        result.music_id = music_id
        chart_mapping = {
            'difficulty': lambda x: difficulty_as_int.get(x.tag.upper()),
            'level': {'key': 'difnum', 'fun': int},
            'illustrator': None,
            'effected_by': None,
            'limited': {'fun': int},
        }
        xml_utils.extractor(xml, chart_mapping, result)
        return result

    @property
    def diff_name(self):
        return difficulty_repr.get(self.difficulty)
