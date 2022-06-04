import os
import pytest
import tempfile
from server import flask
from app.database.connection import init_db
from tests.factories.PackageFactory import PackageFactory


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


@pytest.fixture
def package_factory(application):
    return PackageFactory(application)
