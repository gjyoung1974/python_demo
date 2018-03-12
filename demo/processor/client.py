from urllib.parse import urljoin, urlunsplit

import requests
from flask import current_app

from .helpers import dumps


def charge(payload):
    root_url = current_app.config['VGS_PROCESSOR_ROOT_URL']
    url = urljoin(root_url, '/charge')
    proxy_url = urlunsplit(
        ('https',
         '{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_URL}:{PROXY_PORT}'.format(
             PROXY_USERNAME=current_app.config['VGS_PROXY_USERNAME'],
             PROXY_PASSWORD=current_app.config['VGS_PROXY_PASSWORD'],
             PROXY_URL=current_app.config['VGS_PROXY_URL'],
             PROXY_PORT=current_app.config['VGS_PROXY_PORT']
             ),
         '', None, None))
    r = requests.post(
        url,
        data=dumps(payload),
        headers={"Content-type": "application/json"},
        proxies={"https": proxy_url},
        verify='demo/static/cert.pem'
        )
    return r