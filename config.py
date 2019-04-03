import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, Api

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}/test.db'.format(os.path.join(BASEDIR))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
# app.config['SECRET_KEY'] = "SECRET"
db = SQLAlchemy(app=app)
