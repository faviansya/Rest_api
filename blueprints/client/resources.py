import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required

from . import *

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):

    def __init__(self):
        pass

    def get(self, client_id = None):
        if client_id == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('status', type = str, location = 'args')
            parser.add_argument('client_id', type = str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Client.query

            if args['status'] is not None:
                qry = qry.filter(Client.status.like("%"+args['status']+"%"))
            if args['client_id'] is not None:
                qry = qry.filter(Client.id.like("%"+args['client_id']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Client.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = Client.query.get(client_id)
            if qry is not None:
                return marshal(qry, Client.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    def delete(self, client_id):
        qry = Client.query.get(client_id)
        
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def put(self, client_id):
        qry = Client.query.get(client_id)

        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json')
        parser.add_argument('password', location = 'json')
        parser.add_argument('status', location = 'json')
        args = parser.parse_args()
        
        if args['username'] is not None:
            qry.username = args['username']
        if args['password'] is not None:
            qry.password = args['password']
        if args['status'] is not None:
            qry.status = args['status']

        db.session.commit()
        if qry is not None:
            return marshal(qry, Client.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('status', location = 'json', required = True)
        args = parser.parse_args()

        clients = Client(None, args['username'], args['password'], args['status'])
        db.session.add(clients)
        db.session.commit()

        return marshal(clients, Client.response_field), 200, {'Content_type' : 'application/json'}

api.add_resource(ClientResource, '', '/<int:client_id>')