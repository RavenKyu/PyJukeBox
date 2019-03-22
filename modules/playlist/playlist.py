from flask import render_template, Blueprint, jsonify, request
from common.utils import request_wants_json, ReturnValue
playlist = Blueprint(
    'playlist', #name of module
    __name__,
    template_folder='templates' # templates folder
)

@playlist.route('/', methods=['GET','PUT'])
def index():
    data = [{'nickname': "Raven", 'playlist': [
        {"artist": "ESense", "title": "Writer`s Block", "url":
            "http://hello.com"},
        {"artist": "ESense", "title": "Writer`s Block", "url":
            "http://hello.com"}
    ]},
    {'nickname': "Raven", 'playlist': [
        {"artist": "ESense", "title": "Writer`s Block", "url":
            "http://hello.com"},
        {"artist": "ESense", "title": "Writer`s Block", "url":
            "http://hello.com"}
    ]}]

    if request.method == 'PUT':
        data = request.form['nm']

    if request.method == 'GET':
        pass
        # data = request.args.get('nm')
    if request_wants_json():
        return jsonify(ReturnValue(data))
    return render_template('playlist.html', data=data)

@playlist.route('/<nickname>')
def user(nickname):

    pl = [
        {"artist": "ESense", "title": "Writer`s Block", "url":
            "http://hello.com"},
        {"artist": "ESense", "title": "Writer`s Block", "url":
            "http://hello.com"}
    ]
    data = {"nickname": nickname, "playlist": pl}
    retv = ReturnValue(data)
    if request_wants_json():
        return jsonify(retv)
    return render_template('playlist_user.html', data=data)