import os
import pytest
import tempfile
from server import flask
from app.database.connection import init_db, get_db


@pytest.fixture
def application():
    db_fd, db_path = tempfile.mkstemp()
    flask.config.from_mapping({
        'DB_PATH': db_path,
    })

    with flask.app_context():
        init_db()

    yield flask

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(application):
    return application.test_client()


@pytest.fixture
def runner(application):
    return application.test_cli_runner()


class Factory:
    def __init__(self, app):
        self.app = app

    def insert_packages(self):
        with self.app.app_context():
            db = get_db()
            with self.app.open_resource('tests/data/dummy_packages.sql') as f:
                db.executescript(f.read().decode('utf8'))

    def insert_downloads(self):
        return


@pytest.fixture
def factory(application):
    return Factory(application)
