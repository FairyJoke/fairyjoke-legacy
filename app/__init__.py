import importlib
import logging
import os
from flask import Flask, Blueprint, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model as FlaskModel
from sqlalchemy import MetaData

class Model(FlaskModel):
    def __repr__(self):
        result = super().__repr__()
        if hasattr(self, 'key'):
            result = result[:-1] + f' key={self.key}' + result[-1:]
        return result

db = SQLAlchemy(
    metadata=MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }),
    model_class=Model,
)
migrate = Migrate()

from . import cli
from .config import Config
from .json_encoder import CustomJSONEncoder

def is_strict():
    return request.args.get('strict', False)

def init_blueprint(module, prefix=False, **kwargs):
    name = module[len(__name__) + 1:]
    if prefix:
        if not isinstance(prefix, str):
            prefix = '/' + module.split('.')[-1]
        kwargs['url_prefix'] = prefix
    return Blueprint(name, module,
        static_folder='static',
        template_folder='templates',
        **kwargs
    )

def create_app(config_path='../fairyjoke.cfg'):
    os.environ['CONFIG_FILE'] = os.environ.get('CONFIG_FILE', config_path)
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_envvar('CONFIG_FILE', True)
    cli.init_app(app)
    db.init_app(app)

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    app.json_encoder = CustomJSONEncoder

    for module in ['front', 'main', 'sdvx']:
        module = importlib.import_module('{}.{}'.format(__name__, module))
        app.register_blueprint(module.bp)

    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)

    return app
