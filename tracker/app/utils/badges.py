from app.utils.enumerable import Enumerable


class FCBadges(Enumerable):
    _ALMOST_LIMIT = 3

    FC = 'FULLCOMBO'
    ALMOST_FC = 'ALMOST FULLCOMBO'

    @classmethod
    def from_score(cls, score):
        judges = score.judges_obj
        if judges.miss == 0:
            return [cls.FC]
        if judges.miss <= cls._ALMOST_LIMIT:
            return [cls.ALMOST_FC]
        return []
