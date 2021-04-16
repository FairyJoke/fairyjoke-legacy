from app import init_blueprint

bp = init_blueprint(__name__)

def build_hierarchy(*args):
    '''
    Returns a list of displayable links, meant to be displayed in a breadcrumb
    :param args: Routes
    '''
    from flask import url_for

    titles = {
        '.index': 'Home',
    }
    return [{
        'text': titles.get(x) if x in titles else x.split('.')[-1].capitalize(),
        'url': url_for(x),
        'route': x,
    } for x in args]

from .routes import index
