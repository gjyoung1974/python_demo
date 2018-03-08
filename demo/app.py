from flask import flash, Flask, render_template, request, url_for, g, redirect
import requests
from werkzeug.datastructures import ImmutableMultiDict
import json

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 'pydemo.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# {"name": "Bob Jones", "billing_address": "1 Dr Carlton B Goodlett Pl, San Francisco, CA 94102", "card-number": "5105105105105100", "card-expiration-date": "12/20", "card-security-code": "123"}

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
        print('i am here')
        print(self)
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
            flash('%s cards were charged successfully.'.format(count))
        except Exception as ex:
            flash('Failed to approve users. %s'.format(ex))



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


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(host='0.0.0.0', debug=True, port=8080)
