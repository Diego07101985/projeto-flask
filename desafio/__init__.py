# -*- coding: utf-8 -*-
import json
import datetime
import os

from flask.logging import default_handler
import logging


from flask import Flask
import click
from flask.cli import with_appcontext
from bson.objectid import ObjectId
from logging.config import dictConfig
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


__version__ = (1, 0, 0, "dev")

db = SQLAlchemy()
migrate = Migrate()


def init_db():
    db.drop_all()
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # some deploy systems set the database url in the environ
    db_url = os.environ.get("DATABASE_URL")

    if db_url is None:
        # default to a sqlite database in the instance folder
        db_path = os.path.join(app.instance_path, "desafio.sqlite")
        db_url = f"sqlite:///{db_path}"
        # ensure the instance folder exists
        os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        # default secret that should be overridden in environ or config
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # initialize Flask-SQLAlchemy and the init-db command
    app.cli.add_command(init_db_command)

    db.init_app(app)
    migrate.init_app(app, db)

    return app


app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

for logger in (
    app.logger,
    logging.getLogger('sqlalchemy'),
):
    logger.addHandler(default_handler)


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app.debug = True
# client = MongoClient('mongodb://localhost:27017/')
# db = client['test']

# db = create_engine('sqlite:///desafio.db', echo=True)
# Session = sessionmaker(bind=db)
# Base = declarative_base()


# class DataAccessLayer:
#     def __init__(self, conn_string):
#         self.engine = None
#         self.session = None
#         self.conn_string = conn_string
#         self.Base = None

#     def connect(self):
#         self.engine = create_engine(self.conn_string)
#         self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
#         # self.session = self.Session()
#         self.Base.metadata.create_all(self.engine)

# with app.app_context():
#     init_db()
#     user = User(username="julio", email='l@l')
#     db.session.add_all(
#         (
#             user,
#             User(username="paulo", email='p@p'),
#         )
#     )
#     db.session.commit()


@contextmanager
def session_scope(expire=False):
    """Provide a transactional scope around a series of operations."""
    session = db.session()
    session.expire_on_commit = False
    try:
        yield session

        app.logger.info(f'Sessão foi iniciada {session}')
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        app.logger.info(f'Sessão foi iniciada {session}')

from desafio import controllers

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)