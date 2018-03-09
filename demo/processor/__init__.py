from flask import Blueprint, Response as FlaskResponse

from . import helpers as h
from . import client

processor = Blueprint('processor', __name__)

@processor.route('/charge', methods=('POST',))
def view_post():
    """Returns POST Data."""

    return h.jsonify(h.get_dict(
        'url', 'args', 'form', 'data', 'origin', 'headers', 'files', 'json'))


class _ClientResponse(FlaskResponse):

    def json(self):
        if self.content_type != 'application/json':
            error = 'content_type is not application/json! Got {0} instead.'
            raise TypeError(error.format(self.content_type))
        return h.loads(self.data.decode('utf-8'))


def on_register(app):
    app.json_encoder = h.JSONEncoder
    app.response_class = _ClientResponse
    return app
