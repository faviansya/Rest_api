import requests
import logging
import json
from flask import Flask
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
import datetime
import random
from . import *

bp_Song = Blueprint('Song', __name__)
api = Api(bp_Song)


class PublicGetCurrentSong(Resource):
    # wio_apikey = '001de4440e814c16bc45197fd601ef9d'

    @jwt_required
    def get(self, current_mood=None):
        jwtclaim = get_jwt_claims()
        if (current_mood == None):

            self.timenow = int(datetime.datetime.now().strftime("%H"))
            if (self.timenow >= 6 and self.timenow <= 14):
                qry = Playlist.query.filter_by(time = 'pagi')
                if jwtclaim['status'] == 'public' :
                    qry = Playlist.query.filter_by(time = 'pagi').filter_by(status = 'public')
                self.data = self.check('pagi',qry)
            elif (self.timenow >= 15 and self.timenow <= 22):
                qry = Playlist.query.filter_by(time = 'siang')
                if jwtclaim['status'] == 'public' :
                    qry = Playlist.query.filter_by(time = 'siang').filter_by(status = 'public')
                self.data = self.check('siang',qry)
            else:
                qry = Playlist.query.filter_by(time = 'malam')
                if jwtclaim['status'] == 'public' :
                    qry = Playlist.query.filter_by(time = 'malam').filter_by(status = 'public')
                self.data = self.check('malam',qry)
            return self.data, 200

        qry = Playlist.query.filter_by(mood = current_mood)

        if jwtclaim['status'] == 'public' :
            qry = Playlist.query.filter_by(mood = current_mood).filter_by(status = 'public')

        current_mood = current_mood.lower()
        data = self.check(current_mood,qry)

        # if current_mood == 'senang':
        #     data = self.check('senang',qry)
        # elif current_mood == 'sedih':
        #     data = self.check('sedih',qry)
        # elif current_mood == 'mager':
        #     data = self.check('mager',qry)
        # elif current_mood == 'produktif':
        #     data = self.check('produktif',qry)
        # elif current_mood == 'nostalgia':
        #     data = self.check('nostalgia',qry)

        return data,200

    def put(self):
        return 'a'

    def check(self, current_mood, qry):
        self.full_data = []

        for row in qry:
            self.gif = self.getgif(current_mood)
            self.joke = self.getJoke()
            self.wio_host = 'https://api.spotify.com/v1/playlists/'
            songlist = marshal(row, Playlist.response_field)
            self.wio_host = self.wio_host + songlist['playlist']
            rq = requests.get(self.wio_host,
                        headers={'Authorization': 'Bearer BQDJhMC7RUthX0GcVY2jqFeq-bj0vJIDdZW3Tdme2L-OtPkhZZUkF2HZoEIMIV6UcSxiNGkrxeko0OPqK0lVLwem5B93hpQ1QbyxdUSwpVhywTWjIle170DfiKGqeDwtPwdIkHR8Hd43NVf0Vpe_3AEnsJ73wT56QQ'})
            lagu = rq.json()
            self.data = []
            for datas in range(len(lagu['tracks']['items'])): 
                self.data.append({'judul': lagu['tracks']['items'][datas]['track']['name'], 
                'penyanyi':lagu['tracks']['items'][datas]['track']['album']['artists'][0]['name']})

            self.full_data.append({'playlist':lagu['name'],'small-Gif-For-you':self.gif,'Want a Joke?': self.joke['setup'],'answer;':self.joke['punchline'],'list_lagu': self.data})

        return self.full_data

    def getgif(self,data):
        self.gif_host = 'https://api.giphy.com/v1/gifs/search'
        self.rq = requests.get(self.gif_host,
            params={'api_key': 'b9qdTqZbEIJgeFprGELsYGKPF2y7o9hJ', 'q':'random', 'limit':10 })
        if(data == 'senang'):
            self.rq = requests.get(self.gif_host,
                params={'api_key': 'b9qdTqZbEIJgeFprGELsYGKPF2y7o9hJ', 'q':'happy', 'limit':10 })
        elif(data == 'sedih'):
            self.rq = requests.get(self.gif_host,
                params={'api_key': 'b9qdTqZbEIJgeFprGELsYGKPF2y7o9hJ', 'q':'semangat', 'limit':10 })
        elif(data == 'mager'):
            self.rq = requests.get(self.gif_host,
                params={'api_key': 'b9qdTqZbEIJgeFprGELsYGKPF2y7o9hJ', 'q':'come get up', 'limit':10 })
        elif(data == 'nostalgia'):
            self.rq = requests.get(self.gif_host,
                params={'api_key': 'b9qdTqZbEIJgeFprGELsYGKPF2y7o9hJ', 'q':'nostalgic', 'limit':10 })
        gif = self.rq.json()
        return gif['data'][random.randrange(0,9)]['images']['preview']['mp4']
    
    def getJoke(self):
        self.joke_host = 'https://official-joke-api.appspot.com/jokes/random'
        self.rq = requests.get(self.joke_host)
        joke = self.rq.json()
        print (joke)
        print ('joke')
        return joke


api.add_resource(PublicGetCurrentSong, '/mood', '/mood/<current_mood>', endpoint='todo_ep')
