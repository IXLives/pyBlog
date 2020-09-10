import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext

# g
# g is a unique request object used to store data that might be accessed by multiple functions during the request.
# Stored and re-used if called during the same request instead of creating a new connection


def get_db():
    # Connect to the database, or create it
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    # if a connection exists, close it
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    # Clear existing data and create new tables
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
