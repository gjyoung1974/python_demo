import requests

from .helpers import dumps



def charge(payload):
    r = requests.post('http://localhost:8080/charge', data=dumps(payload))
    return r