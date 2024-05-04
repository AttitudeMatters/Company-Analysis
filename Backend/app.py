import json

from flask import Flask, request
from flask_cors import CORS

from Dataflow import analyze
app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello_world():  # put application's code here
    print(request.headers)
    result = analyze(request.headers.get('Company-Name'), request.headers.get('Year'))
    return json.dumps({'result': result})


if __name__ == '__main__':
    app.run()
