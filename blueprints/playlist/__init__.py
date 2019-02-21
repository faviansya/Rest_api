import logging
from blueprints import db
from flask_restful import fields

class Member(db.Model):

    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    playlist = db.Column(db.String(255))
    mood = db.Column(db.String(50))
    status = db.Column(db.String(50))
    time = db.Column(db.String(50))
    create_by = db.Column(db.Integer)

    response_field = {
        'id' : fields.Integer,
        'playlist' : fields.String,
        'mood' : fields.String,
        'status' : fields.String
    }

    def __init__(self, id, name, mood, status, time):
        self.id = id
        self.playlist = playlist
        self.mood = mood
        self.status = status
        self.time = time
        self.create_by = create_by

    def __repr__(self):
        return '<Member %r>' % self.id