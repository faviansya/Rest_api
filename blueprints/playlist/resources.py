import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required

from . import *

bp_playlist = Blueprint('playlist', __name__)
api = Api(bp_playlist)

class PlaylistResource(Resource):

    def __init__(self):
        pass

    def get(self, playlist_id = None):
        if playlist_id == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('mood', type = str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = playlist.query

            if args['mood'] is not None:
                qry = qry.filter_by(mood = args['status'])
            else:
                qry = qry.filter_by(time)

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, playlist.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = playlist.query.get(playlist_id)
            if qry is not None:
                return marshal(qry, playlist.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    def delete(self, playlist_id):
        qry = playlist.query.get(playlist_id)
        
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def put(self, playlist_id):
        qry = playlist.query.get(playlist_id)

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
            return marshal(qry, playlist.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('status', location = 'json', required = True)
        args = parser.parse_args()

        playlists = playlist(None, args['username'], args['password'], args['status'])
        db.session.add(playlists)
        db.session.commit()

        return marshal(playlists, playlist.response_field), 200, {'Content_type' : 'application/json'}

api.add_resource(playlistResource, '', '/<int:playlist_id>')