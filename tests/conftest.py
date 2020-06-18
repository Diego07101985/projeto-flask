
try:
    import sys
    import os

    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../desafio'
            )
        )
    )
except:
    raise

import pytest
from desafio import create_app
from desafio import init_db
from desafio import db
from desafio.models import User


@pytest.fixture(scope="session")
def app():
    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory"})

    with app.app_context():
        init_db()

    app.app_context().push()

    yield app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app):
    return app.test_cli_runner()
