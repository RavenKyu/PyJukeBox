from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

################################################################################
class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    registered_date = db.Column(db.DateTime(timezone=True), default=func.now())

    # ==========================================================================
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    # ==========================================================================
    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.name, self.password, self.email)


################################################################################
class UserPlayListIndex(db.Model):
    __tablename__ = 'user_play_list_index'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    name = db.Column(db.String(80), nullable=False)

    registered_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.relationship(
        "User", backref=db.backref('user_play_list_index', order_by=id))

    # ==========================================================================
    def __init__(self, name):
        self.name = name

    # ==========================================================================
    def __repr__(self):
        return "<UserPlayListIndex('%s')>" % self.name

################################################################################
class UserPlayList(db.Model):
    __tablename__ = 'user_play_list'
    id = db.Column(db.Integer, primary_key=True)
    play_list_index_id = db.Column(
        db.Integer, db.ForeignKey('user_play_list_index.id'))

    url = db.Column(db.String(1024), nullable=False)
    media_url = db.Column(db.String(1024))
    title = db.Column(db.String(1024))
    thumbnail = db.Column(db.String(1024))
    description = db.Column(db.String(1024))

    registered_date = db.Column(db.DateTime(timezone=True), default=func.now())
    flag_playing = db.Column(db.Boolean)

    play_list_index = db.relationship(
        "UserPlayListIndex",
        backref=db.backref('user_play_list', order_by=id))

    # ==========================================================================
    def __init__(self, name, url, description):
        self.name = name
        self.url = url
        self.description = description

    # ==========================================================================
    def __repr__(self):
        return "<UserPlayList('%s', '%s', '%s')>" % (
            self.name, self.url, self.description)
