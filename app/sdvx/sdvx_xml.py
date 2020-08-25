from datetime import date
def bpmify(x):
    return int(x) / 100

def dateify(x):
    return date.fromisoformat('{}-{}-{}'.format(x[:4], x[4:6], x[6:8]))
