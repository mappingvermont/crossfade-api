from flask import Flask, request, jsonify, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.api import status
#from flask_cors import CORS, cross_origin
import os
import json
from hashids import Hashids
import sys
import logging

#logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)
#cors = CORS(app, resources={r"/collection/*": {"origins": "*"}})
#cors = CORS(app, resources={r"/collection/*": {"origins": "http://xfade.audio/"}})
#app.config.from_object(os.environ['CROSSFADE_APP_SETTINGS'])
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['CROSSFADE_DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///crossfade'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['CORS_HEADERS'] = 'Content-Type'

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

        #output = jsonify({'collection_id': hashid})
        return  jsonify({'collection_id': hashid})

    else:

        resp = Response(status=200)
        resp.headers['Allow'] = 'POST'

        return resp


#        content = {'Allow': 'POST'}
#        return jsonify({'ok': 'ok'})
#        return (content, status.HTTP_200_OK)
#        return status.HTTP_200_OK
#        return {'Allow' : 'POST' }, status.HTTP_200_OK
#        return {'Allow' : 'POST' } , 200
#        return  200

#        output = jsonify({'options': 'ok'})
 #       output = jsonify({'options': 'ok'})

        #return ('', 204)
  #  return output

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
