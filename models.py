from app import db
from sqlalchemy.dialects.postgresql import JSON


# Create collection table
class Collection(db.Model):
    __tablename__ = 'collection'

    # Define primary key integer and collection_json column
    id = db.Column(db.Integer, primary_key=True)
    collection_json = db.Column(JSON)

    def __init__(self, collection_json):
        self.collection_json = collection_json

    def __repr__(self):
        return '<id {}>'.format(self.id)
