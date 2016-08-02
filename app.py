from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
import json
from hashids import Hashids


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
hashids = Hashids(min_length=8)


from models import Playlist


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/new', methods=['POST'])
def new():

    data = json.loads(request.data.decode())
    playlist = Playlist(json_state=data['json_state'])

    db.session.add(playlist)
    
    # http://stackoverflow.com/questions/1316952
    db.session.flush()

    hashid = hashids.encode(playlist.id)
    playlist.hashid = hashid

    db.session.commit()

    return playlist.hashid


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
