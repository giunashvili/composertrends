import sqlite3
from flask import current_app, g
import os


def get_db():
    if 'db' not in g:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db = current_app.config['DB_PATH']
        database_path = os.path.join(base_dir, db)
        g.db = sqlite3.connect(
            database_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db() -> object:
    db = get_db()
    with current_app.open_resource('app/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
