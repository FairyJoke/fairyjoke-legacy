from app import db, xml_utils, serializer
from .. import sdvx_xml

class Music(db.Model):
    __tablename__ = 'sdvx_music'

    INFO_MAPPING = {
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
    charts = db.relationship('Chart', backref='music')

    @classmethod
    def empty(cls):
        result = cls()
        result.id = 0
        for key in cls.INFO_MAPPING:
            setattr(result, key, '???')
        result.extra_diff_type = 2
        return result

    @classmethod
    def from_xml(cls, xml):
        result = cls()
        result.id = int(xml.get('id'))
        xml_utils.extractor(xml.find('info'), cls.INFO_MAPPING, result)
        return result

    def as_dict(self, include_charts=True):
        result = serializer.dictify(self, [
            'id', 'label', 'title', 'title_yomigana', 'artist',
            'artist_yomigana', 'ascii', 'bpm_max', 'bpm_min', 'release_date',
            'background_id', 'genre_id', 'version', 'demo_pri',
            'extra_diff_type',
        ])
        if include_charts:
            from . import Chart
            result['charts'] = {x.difficulty: serializer.dictify(x, [
                'diff_name', 'diff_short', 'jacket_id', 'level', 'illustrator',
                'effected_by', 'limited', 'jacket_small_url',
                'jacket_medium_url', 'jacket_large_url',
            ]) for x in (
                Chart.query.filter_by(music_id=self.id).all()
                if self.id > 0 else (Chart.empty(x) for x in range(1, 6))
            )}
        return result

    def get_music_folder(self):
        return '{}_{}'.format(str(self.id).zfill(4), self.ascii)
