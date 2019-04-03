from flask import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.attributes import QueryableAttribute
from config import db


################################################################################
class BaseModel(db.Model):
    __abstract__ = True

    # ==========================================================================
    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide), _path=("%s.%s" % (_path,
                                                             key.lower()))

                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data


################################################################################
class User(BaseModel):
    __tablename__= 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    modified_at = db.Column(DateTime())
    created_at = db.Column(DateTime(), nullable=False,
                           default=datetime.utcnow)

    _default_fields = ["name", "email"]
    _hidden_fields = ["password"]

    # ==========================================================================
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    # ==========================================================================
    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.name, self.password, self.email)


################################################################################
class UserPlayListIndex(BaseModel):
    __tablename__ = 'user_play_list_index'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    name = Column(String(80), nullable=False)
    modified_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    user = relationship(
        "User", backref=backref('user_play_list_index', order_by=id))

    _default_fields = ["name"]

    # ==========================================================================
    def __init__(self, name):
        self.name = name

    # ==========================================================================
    def __repr__(self):
        return "<UserPlayListIndex('%s')>" % self.name


################################################################################
class UserPlayList(BaseModel):
    __tablename__ = 'user_play_list'
    id = Column(Integer, primary_key=True)
    play_list_index_id = Column(
        Integer, ForeignKey('user_play_list_index.id'))

    url = Column(String(1024), nullable=False)
    media_url = Column(String(1024))
    title = Column(String(1024))
    thumbnail = Column(String(1024))
    description = Column(String(1024))
    modified_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    flag_playing = Column(Boolean)

    play_list_index = relationship(
        "UserPlayListIndex",
        backref=backref('user_play_list', order_by=id))

    _default_fields = ["name", "url", "description"]

    # ==========================================================================
    def __init__(self, name, url, description):
        self.name = name
        self.url = url
        self.description = description

    # ==========================================================================
    def __repr__(self):
        return "<UserPlayList('%s', '%s', '%s')>" % (
            self.name, self.url, self.description)
