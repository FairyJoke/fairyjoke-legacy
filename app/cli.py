import click


def init_app(app):

    @app.cli.command('import')
    @click.option('-d', '--dry', is_flag=True)
    @click.option('--dump', is_flag=True)
    def import_data(dry, dump):
        from app.importer import Importer
        Importer().run(dry=dry, dump=dump)
