import click
from flask.cli import with_appcontext
from app.database.connection import init_db


@click.command('db:refresh')
@with_appcontext
def refresh_database():
    init_db()
    click.echo('Database has been refreshed!')
