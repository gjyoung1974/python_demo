from flask import Flask, render_template, request, url_for, g
import requests
import json




def run_app():
  app = Flask(__name__)

  @app.route('/', methods=["GET", "POST"])
  def index():
      if request.method == 'GET':
          return render_template('index.html')
      else:
          print(request.get_json())
          return render_template('success.html')

  @app.route('/send', methods=['POST'])
  def send():
    data = {
    "name" : request.form['name'],
    "billing_street" : request.form['billing_street'],
    "billing_city" : request.form['billing_city'],
    "billing_state" :  request.form['billing_state'],
    "billing_zip" : request.form['billing_zip'],
    "pan_number" : request.form['pan_number'],
    "pan_exp" : request.form['pan_exp'],
    "pan_cvv" : request.form['pan_cvv']}

    res = requests.post("https://tntrsf2iagd.SANDBOX.verygoodproxy.com", json=data)

    return render_template('success.html')
  return app
