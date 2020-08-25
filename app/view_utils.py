from flask import url_for

def build_hierarchy(*args):
    '''
    Returns a list of displayable links, meant to be displayed in a breadcrumb
    :param args: Routes
    '''
    titles = {
        'main.index': 'Home',
    }
    return [{
        'text': titles.get(x) if x in titles else x.split('.')[-1].capitalize(),
        'url': url_for(x),
        'route': x,
    } for x in args]
