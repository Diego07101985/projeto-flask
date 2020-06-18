
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
    print('Create and configure a new app instance for each test.')
    # create the app with common test config
    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory"})

    # create the database and load test data
    # set _password to pre-generated hashes, since hashing for each test is slow
    # with app.app_context():
    #     db.create_all()
    # print("estou aqui")

    with app.app_context():
        init_db()

    app.app_context().push()

    yield app


@pytest.fixture(scope="session")
def client(app):
    print('A test client for the app.')
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app):
    print('A test runner for the apps Click commands')
    return app.test_cli_runner()
