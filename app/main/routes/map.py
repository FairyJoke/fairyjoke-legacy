from flask import current_app, url_for

from .. import bp

@bp.route('/map')
def map():
    return {
        x.endpoint: x.rule
        for x in current_app.url_map.iter_rules()
    }
