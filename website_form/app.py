from flask import Flask, render_template, request, url_for, g
import requests
from werkzeug.datastructures import ImmutableMultiDict
import json




def run_app():
  app = Flask(__name__)

  @app.route('/', methods=["GET", "POST"])
  def index():
      if request.method == 'GET':
          return render_template('index.html')
      else:

          imm = request.values
          dic = imm.to_dict(flat=True)
          json_data = json.dumps(dic)
          print (json_data)
          r = requests.post(
          'https://httpbin.verygoodsecurity.io/post',
          data=json_data,
          headers={"Content-type": "application/json", "VGS-Log-Request": "all"},
          proxies={"https": "https://USuENQQdfR8yhgjdz2x11ydY:9be4303d-f84d-4943-a9c1-164e53c6fbac@tntrsf2iagd.SANDBOX.verygoodproxy.com:8080"},
          verify='website_form/cert.pem'
          )

          print(r.json()['data'])

          return render_template('success.html')

  @app.route('/send', methods=['POST'])
  def send():

    return render_template('success.html')
  return app
