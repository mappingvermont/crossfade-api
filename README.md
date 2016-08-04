# Crossfade-API

A basic REST API to allow [crossfade.audio](http://crossfade.audio) to create unique URL hashes for playlists.

Adapted from [this great Flask tutorial](https://realpython.com/blog/python/flask-by-example-part-1-project-setup/).

### Installation

1. Clone the repo
2. virtualenv env
3. source env/bin/activate
4. pip install -r requirements.txt
5. deactivate
6. pip install autoenv==1.0.0

#### Set local variables
1. touch .env

2. Edit .env to add local settings

`source env/bin/activate`  
`export APP_SETTINGS="config.ProductionConfig"`  
`export DATABASE_URL="postgresql:///crossfade"`

#### Update .bashrc
1. echo "source `which activate.sh`" >> ~/.bashrc
2. source ~/.bashrc

### Run it!

`python manage.py runserver`
