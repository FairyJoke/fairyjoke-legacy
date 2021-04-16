import click


def init_app(app):

    @app.cli.command('import')
    @click.option('-d', '--dry', is_flag=True)
    def import_data(dry):
        from app.importer import Importer
        Importer().run(dry=dry)
