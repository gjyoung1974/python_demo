import argparse
import json
import sys
import traceback
from urllib.parse import urlunsplit, urlparse

import os
import requests
from flask import flash, Flask, render_template, request
from flask_admin import Admin
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

import processor
from flask_admin_material import setup_templates as setup_admin_material_theme


app = Flask(__name__)
app.register_blueprint(processor.processor)
app = setup_admin_material_theme(app)
app = processor.on_register(app)


app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 'pydemo.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    billing_address = db.Column(db.String(100))
    card_number = db.Column(db.String(100))
    card_expiration = db.Column(db.String(100))
    card_security_code = db.Column(db.String(100))

    @classmethod
    def from_dict(cls, kwargs):
        payment_obj = cls()
        payment_obj.name = kwargs['name']
        payment_obj.billing_address = kwargs['billing_address']
        payment_obj.card_number = kwargs['card-number']
        payment_obj.card_expiration = kwargs['card-expiration-date']
        payment_obj.card_security_code = kwargs['card-security-code']
        return payment_obj

    def charge(self):
        response = processor.client.charge({'card': self.card_number})
        response.raise_for_status()
        print(response.json())
        return True


class PaymentAdmin(ModelView):

    @action('charge', 'Charge', 'Are you sure you want to charge this card?')
    def action_charge(self, ids):
        try:
            query = Payment.query.filter(Payment.id.in_(ids))
            count = 0
            for payment_entry in query.all():
                payment_entry.charge()
                count += 1
            flash('{count} cards were charged successfully.'.format(count=count))
        except Exception as ex:
            print(''.join(traceback.format_exception(None,ex, ex.__traceback__)),
                  file=sys.stderr, flush=True)
            flash('Failed to approve users. {error}'.format(error=ex), category='error')


admin = Admin(app, name='pydemo', template_mode='bootstrap3')
admin.add_view(PaymentAdmin(Payment, db.session))

def redaction(dic):
    return render_template('show_redacted.html', data = dic)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method =='POST':
        imm = request.values
        dic = imm.to_dict(flat=True)
        json_data = json.dumps(dic)
        print(json_data)
        return redaction(dic)

@app.route('/show_redacted', methods=['GET'])
def show_redacted():
    render_template('show_redacted.html')

@app.route('/revealed_data', methods=['POST'])
def revealed_data():
    imm = request.values['data']
    data = imm.replace("'", '"')
    json_data = data
    print(json_data)
    requests.post(
    'https://third-party.herokuapp.com/',
    data=json_data,
    headers={"Content-type": "application/json"},
    proxies={"https": "https://USuENQQdfR8yhgjdz2x11ydY:9be4303d-f84d-4943-a9c1-164e53c6fbac@tntrsf2iagd.SANDBOX.verygoodproxy.com:8080"},
    verify='demo/static/cert.pem'
    )
    # values = r.json()['data']
    # json_acceptable_string = values.replace("'", "\"")
    # vals = json.loads(json_acceptable_string)
    return render_template('index.html')

@app.route('/payment', methods=["GET", "POST"])
def payment():
    if request.method == 'GET':
        return render_template('payment.html')
    elif request.method =='POST':
        imm = request.values
        dic = imm.to_dict(flat=True)
        payment_entry = Payment.from_dict(dic)
        db.session.add(payment_entry)
        db.session.commit()
        json_data = json.dumps(dic)
        print(json_data)
        return redaction(dic)


def create_parser():
    parser = argparse.ArgumentParser(description="VGS Demo", prog="pydemo")

    parser.add_argument('--init-db', dest='init_db', action='store_true',
                        help="re-initializes the database")

    parser.add_argument('--host', dest='server_host', action='store',
                        default='0.0.0.0', help="sets the server host")

    parser.add_argument('--port', dest='server_port', action='store', type=int,
                        default=8080, help="sets the server port")

    parser.add_argument('--debug', dest='server_debug', action='store_true',
                        default=False, help="turns on debug mode")

    parser.add_argument('--processor-root-uri', dest='processor_root_uri',
                        help="sets the processor uri (http(s?)://{HOST}(:{PORT})?")

    parser.add_argument('--vgs-proxy-uri', dest='vgs_proxy_uri',
                        help="configures the VGS proxy uri")

    return parser


def start_server(parsed_args):
    app.run(host=parsed_args.server_host,
            debug=parsed_args.server_debug,
            port=parsed_args.server_port,
            threaded=True)


def init_db(drop=False):
    if drop:
        db.drop_all()
    db.create_all()


def main(pa):
    if pa.init_db:
        init_db(drop=True)

    pr = ('http','{0}:{1}'.format(pa.server_host, pa.server_port), '',
          None, None)

    app.config['VGS_PROCESSOR_ROOT_URL'] = urlunsplit(pr)
    if pa.processor_root_uri:
        app.config['VGS_PROCESSOR_ROOT_URL'] = pa.processor_root_uri

    proxy_uri = None
    for k in ('http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY'):
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

