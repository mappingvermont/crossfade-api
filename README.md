# Crossfade-API

A basic REST API to allow [xfade.audio](http://xfade.audio) to create unique URL hashes for playlists.

Listens for `POST` requests to your-api-url.com/collections/new. Saves whatever JSON is posted in the body to a postgres database and returns a hashID (i.e. lkj902ad).

A `GET` request to your-api-url.com/collections/lkj902ad will return the JSON that was originally POSTed.

Adapted from [this great Flask tutorial](https://realpython.com/blog/python/flask-by-example-part-1-project-setup/).

### Installation
`pip install -r requirements.txt`

`export APP_SETTINGS="config.DevelopmentConfig"`

Create config.py:
```
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'your-secret-key-here'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///crossfade'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///crossfade'
```

### Run it
`python manage.py runserver`
