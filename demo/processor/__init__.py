from flask import Blueprint

from . import helpers as h
from . import client

processor = Blueprint('processor', __name__)

@processor.route('/charge', methods=('POST',))
def view_post():
    """Returns POST Data."""

    return h.jsonify(h.get_dict(
        'url', 'args', 'form', 'data', 'origin', 'headers', 'files', 'json'))


def on_register(app):
    app.json_encoder = h.JSONEncoder
    return app
