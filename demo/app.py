from flask import Flask, render_template, request, url_for, g, redirect
import requests
from werkzeug.datastructures import ImmutableMultiDict
import json





app = Flask(__name__)

def redaction(dic):
return render_template('show_redacted.html', data = dic)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        imm = request.values
        dic = imm.to_dict(flat=True)
        json_data = json.dumps(dic)
        print(json_data)
        return redaction(dic)

@app.route('/show_redacted', methods=['GET'])
def show_redacted():
    return render_template('show_redacted.html')

@app.route('/revealed_data', methods=['POST'])
def revealed_data():
    imm = request.values['data']
    data = imm.replace("'", '"')
    json_data = data
    print(json_data)
    r = requests.post(
    'https://httpbin.verygoodsecurity.io/post',
    data= json_data,
    headers={"Content-type": "application/json"},
    proxies={"https": "https://USuENQQdfR8yhgjdz2x11ydY:9be4303d-f84d-4943-a9c1-164e53c6fbac@tntrsf2iagd.SANDBOX.verygoodproxy.com:8080"},
    verify='website_form/cert.pem'
    )
    values = r.json()['data']
    json_acceptable_string = values.replace("'", "\"")
    vals = json.loads(json_acceptable_string)
        return render_template('revealed_data.html', data = vals)

return app

if __name__ == "__main__":
  app.run()
