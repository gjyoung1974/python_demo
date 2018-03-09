from flask import current_app

from .helpers import dumps


def _client():
    # or this could be requests
    return current_app.test_client()


def charge(payload):
    r = _client().post('/charge', data=dumps(payload))
    return r