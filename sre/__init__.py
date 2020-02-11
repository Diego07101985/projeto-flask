# -*- coding: utf-8 -*-
import os
import json
import datetime
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, jsonify
from pymongo import MongoClient
from logging.config import dictConfig


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
client = MongoClient('mongodb://localhost:27017/')
collection = client['test-database']
from sre import controllers

