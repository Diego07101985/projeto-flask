# -*- coding: utf-8 -*-

import json
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from flask import Flask
from bson.objectid import ObjectId
from logging.config import dictConfig
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

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


class DataAccessLayer:
    def __init__(self, conn_string):
        self.engine = None
        self.session = None
        self.conn_string = conn_string
        self.Base = None

    def connect(self):
        self.engine = create_engine(self.conn_string)
        self.Session = sessionmaker(bind=self.engine)
        # self.session = self.Session()
        self.Base.metadata.create_all(self.engine)


dal = DataAccessLayer('sqlite:///desafio.db')
Base = declarative_base()
dal.Base = Base

from src import controllers