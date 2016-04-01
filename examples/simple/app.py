# -*- coding: utf-8 -*-
'''
    Simple Example App of Flask-Pourer
'''
from flask import Flask
from flask.ext.pymongo import PyMongo
from flask.ext.pourer import Pourer

# Init App
app = Flask(__name__)
# Init PyMongo
mongo = PyMongo(app)
# Init Pourer
pourer = Pourer(app, mongo)

if __name__ == "__main__":
    app.run()
