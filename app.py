from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import os
import json
from hashids import Hashids
import sys

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
hashids = Hashids(min_length=8)


from models import Collection


@app.route('/collection/new', methods=['POST'])
def new():

    data = json.loads(request.data.decode())
    collection = Collection(collection_json=data)

    db.session.add(collection)
    
    # http://stackoverflow.com/questions/1316952
    db.session.flush()

    hashid = hashids.encode(collection.id)

    db.session.commit()

    return jsonify({'collection_id': hashid})


@app.route('/collection/<hash_id>', methods=['GET'])
def get_collection(hash_id):

    unique_id = hashids.decode(hash_id)

    collection = Collection.query.filter_by(id=unique_id).first_or_404()

    print collection.collection_json

    return jsonify(collection.collection_json)


if __name__ == '__main__':
    app.run()
