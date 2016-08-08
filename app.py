from flask import Flask, request, jsonify, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.api import status
import os
import json
from hashids import Hashids
import sys
import logging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///crossfade'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
hashids = Hashids(min_length=8)


from models import Collection


@app.route('/collection/new', methods=['POST', 'OPTIONS'])
def new():

    if request.method == 'POST':

        data = json.loads(request.data.decode("utf-8"))
        collection = Collection(collection_json=data)

        db.session.add(collection)
    
        # http://stackoverflow.com/questions/1316952
        db.session.flush()

        hashid = hashids.encode(collection.id)

        db.session.commit()

        return  jsonify({'collection_id': hashid})

    else:
        # OPTIONS request
        resp = Response(status=200)
        resp.headers['Allow'] = 'POST'

        return resp


@app.route('/collection/<hash_id>', methods=['GET'])
def get_collection(hash_id):

    unique_id = hashids.decode(hash_id)

    collection = Collection.query.filter_by(id=unique_id).first_or_404()

    print collection.collection_json

    return jsonify(collection.collection_json)


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response


if __name__ == '__main__':
    app.run()
