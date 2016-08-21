from flask import Flask, request, jsonify, Response
from flask.ext.sqlalchemy import SQLAlchemy
import json
import os
from hashids import Hashids

app = Flask(__name__)

# Point flask to config.py-- in local dir on development, but
# in wsgi external dir on production machine
app.config.from_object(os.environ['CROSSFADE_APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
hashids = Hashids(min_length=8)

from models import Collection


@app.route('/collection/new', methods=['POST', 'OPTIONS'])
def new():
    if request.method == 'POST':

        # Load the JSON that's POSTed to the API
        data = json.loads(request.data.decode("utf-8"))

        # Create a new row in the collection table with this data
        collection = Collection(collection_json=data)
        db.session.add(collection)

        # Grab the unique ID that's generated (collection.id)
        # http://stackoverflow.com/questions/1316952
        db.session.flush()

        # Convert this unique ID to a pretty hashid
        # i.e. db collection.id 50 -> Jxbo2jag
        hashid = hashids.encode(collection.id)

        # Commit these changes
        db.session.commit()

        # Return the hashid to the front end to be added to the URL
        return jsonify({'collection_id': hashid})

    else:
        # OPTIONS request
        # Required for backbone.js, pre POST request
        resp = Response(status=200)
        resp.headers['Allow'] = 'POST'

        return resp


@app.route('/collection/<hash_id>', methods=['GET'])
def get_collection(hash_id):

    # Decode the hashID submitted to a standard integer/collectionID
    collect_id = hashids.decode(hash_id)

    # Query the collection table by collect_id
    collection = Collection.query.filter_by(id=collect_id).first_or_404()

    # print collection.collection_json

    # Return whatever JSON was first POSTed by the crossfade app
    return jsonify(collection.collection_json)


# Add CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

    return response


if __name__ == '__main__':
    app.run()
