import logging
from blueprints import db
from flask_restful import fields

class Client(db.Model):

    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    status = db.Column(db.String(25))

    response_field = {
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'status' : fields.String
    }

    def __init__(self, id, username, password, status):
        self.id = id
        self.username = username
        self.password = password
        self.status = status

    def __repr__(self):
        return '<Client %r>' % self.id