import os
import tempfile

import pytest
from diary import create_app
from diary.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # creates and opens a temporary file
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        # enable test mode in flask
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
# Tests will use the client to make requests to the application without running the server.
def client(app):
    return app.test_client()


@pytest.fixture
#  creates a runner that can call the Click commands registered with the application.
def runner(app):
    return app.test_cli_runner()

# test auth login and logout functions
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)