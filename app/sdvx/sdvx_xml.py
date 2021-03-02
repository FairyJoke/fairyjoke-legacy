from datetime import date

def bpmify(x):
    return int(x) / 100

def dateify(x):
    return date.fromisoformat('{}-{}-{}'.format(x[:4], x[4:6], x[6:8]))

TRANSLATION_TABLE = str.maketrans(
    '曦曩齷罇驩驫騫齲齶骭龕',
    'àèéêØāá♥♡ü€'
)

def translate(x):
    return x.translate(TRANSLATION_TABLE)
