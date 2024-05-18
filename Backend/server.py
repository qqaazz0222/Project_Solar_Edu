import io
import os
from flask import Flask, jsonify, request, render_template
from flask import make_response
from flask_cors import CORS, cross_origin
import json
from operator import itemgetter
from __solar__ import generate

app = Flask(__name__)
CORS(app,origins=['*'])
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def check():
    return {"msg": "Server is Working!!"}

@app.route('/gen', methods=['POST'])
@cross_origin()
def gen():
    vid = itemgetter('vid')(request.json)
    response = generate(vid)
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5174, debug=True)