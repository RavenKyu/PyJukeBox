from flask import request
import json


class ReturnValue(dict):
    def __init__(self, value):
        dict.__init__(self)
        self['data'] = value

    @property
    def json(self):
        return json.dumps(self)


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']
