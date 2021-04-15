from flask import render_template

from .. import bp, build_hierarchy

@bp.route('/')
def index():
    return render_template('index.html',
        hiearchy=build_hierarchy('.index'),
   )
