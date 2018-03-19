import argparse
import os
from urllib.parse import urlunsplit, urlparse

from flask import Flask

import persistence
import processor
import payment
from flask_admin_material import setup_templates as setup_admin_material_theme


app = Flask(__name__)
# app = setup_admin_material_theme(app)

app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 'pydemo.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

persistence.init_app(app)
processor.init_app(app)
payment.init_app(app)


def create_parser():
    parser = argparse.ArgumentParser(description="VGS Demo", prog="pydemo")

    parser.add_argument('--init-db', dest='init_db', action='store_true',
                        help="re-initializes the database")

    parser.add_argument('--host', dest='server_host', action='store',
                        default='0.0.0.0', help="sets the server host")

    parser.add_argument('--port', dest='server_port', action='store', type=int,
                        default=int(os.environ.get('PORT', 8080)), help="sets the server port")

    parser.add_argument('--debug', dest='server_debug', action='store_true',
                        default=False, help="turns on debug mode")

    parser.add_argument('--processor-root-uri', dest='processor_root_uri',
                        default=os.environ.get("VGS_PROCESSOR_ROOT_URL"),
                        help="sets the processor uri (http(s?)://{HOST}(:{PORT})?")

    parser.add_argument('--vgs-proxy-uri', dest='vgs_proxy_uri',
                        help="configures the VGS proxy uri")

    return parser


def start_server(parsed_args):
    app.run(host=parsed_args.server_host,
            debug=parsed_args.server_debug,
            port=parsed_args.server_port,
            threaded=True)


def main(pa):
    with app.app_context():
        persistence.init_db(drop=pa.init_db)

    pr = ('https','{0}:{1}'.format(pa.server_host, pa.server_port), '',
          None, None)

    app.config['VGS_PROCESSOR_ROOT_URL'] = urlunsplit(pr)
    if pa.processor_root_uri:
        app.config['VGS_PROCESSOR_ROOT_URL'] = pa.processor_root_uri

    proxy_uri = None
    for k in ('http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY',):
        if k in os.environ:
            proxy_uri = os.environ[k]
            break
    else:
        if pa.vgs_proxy_uri:
            proxy_uri = pa.vgs_proxy_uri

    if proxy_uri:
        parsed_uri = urlparse(proxy_uri)
        app.config['VGS_PROXY_USERNAME'] = parsed_uri.username
        app.config['VGS_PROXY_PASSWORD'] = parsed_uri.password
        app.config['VGS_PROXY_PORT'] = parsed_uri.port
        app.config['VGS_PROXY_URL'] = parsed_uri.hostname

    start_server(pa)


if __name__ == "__main__":
    cli_parser = create_parser()
    main(cli_parser.parse_args())
