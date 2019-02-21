import requests
import logging
import json
from flask import Flask
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
import datetime

bp_weather = Blueprint('weather', __name__)
api = Api(bp_weather)


class PublicGetCurrentWeather(Resource):
    # wio_apikey = '001de4440e814c16bc45197fd601ef9d'
    listlagu = {'happy1': '37i9dQZF1DXdPec7aLTmlC',
                    'happy2': '37i9dQZF1DWY8Ogms1X39p',
                    'happy3': '37i9dQZF1DX4uPi2roRUwU',
                    'sedih1': '37i9dQZF1DX0aB3wt1nHwX',
                    'sedih2': '4EoPt05ztUjVaujcWbUL2Z',
                    'sedih3': '37i9dQZF1DX7qK8ma5wgG1',
                    'mager1': '37i9dQZF1DXdHrK6XFPCM1',
                    'mager2': '1zheweB7elTEnOrFuPOgIJ',
                    'mager3': '4FDyczlTchKbIHbJjoMMig',
                    'produktif1': '37i9dQZF1DWV7y9rCVKvZ8',
                    'produktif2': '37i9dQZF1DX8CwbNGNKurt',
                    'produktif3': '0WgsPlbobaxmoUhGbR1TRs',
                    'nostalgia1': '37i9dQZF1DX7a4NCzIrIfF',
                    'nostalgia2': '3jvqYNAY84vsxbHLeNdyGW',
                    'nostalgia3': '37i9dQZF1DXdmXczhgY3oW',
                    }



    def get(self, current_mood=None):
        full_data = []
        if (current_mood == None):
            return {'Message' : 'Masukin Dong Datanya, Moodmu lagi apa?',
                    'Contoh_Mood_Senang': 'Happy,Senang,Bahagia,girang',
                    },200

        current_mood = current_mood.lower()
        if current_mood == 'happy' or current_mood == 'senang' or current_mood == 'bahagia' or current_mood == 'girang':
            self.wio_host = self.checktime('happy')
        elif current_mood == 'sedih' or current_mood == 'nangis' or current_mood == 'galau' or current_mood == 'baper':
            self.wio_host = self.checktime('sedih')
        elif current_mood == 'mager' or current_mood == 'japri' or current_mood == 'gabut':
            self.wio_host = self.checktime('mager')
        elif current_mood == 'produktif' or current_mood == 'semangat' or current_mood == 'olahraga':
            self.wio_host = self.checktime('produktif')
        elif current_mood == 'nostalgia' or current_mood == 'mengenang' or current_mood == 'rindu' or current_mood == 'kangen':
            self.wio_host = self.checktime('nostalgia')

        parser = reqparse.RequestParser()
        parser.add_argument('ip', location='args', default=None)
        args = parser.parse_args()

        rq = requests.get(self.wio_host,
                          headers={'Authorization': 'Bearer BQAdmsQLBNLLhggdopTJFh1tMFHBmtM_BN9qrJ2GF6LDlpBVeGFZE0w2DsYalMQCnbUQfEYre6bKFWh1eA3bhphyu5fq9tBd1uGfazFuXksDoF2lj0DWm8sr3XyWTL5RJM7tBm4vHJfx-4DMrSBVSkFo5J3UjSOT0g'})
        lagu = rq.json()

        for datas in range(len(lagu['tracks']['items'])):
            full_data.append(lagu['tracks']['items'][datas]['track']['name']+' (' +
                             lagu['tracks']['items'][datas]['track']['album']['artists'][0]['name']+')')

        return full_data,200



    def checktime(self, data):
        self.timenow = int(datetime.datetime.now().strftime("%H"))
        self.wio_host = 'https://api.spotify.com/v1/playlists/'
        if (self.timenow >= 6 and self.timenow <= 14):
            self.wio_host = self.wio_host + self.listlagu[(data+'1')]
        elif (self.timenow >= 15 and self.timenow <= 22):
            self.wio_host = self.wio_host + self.listlagu[(data+'2')]
        else:
            self.wio_host = self.wio_host + self.listlagu[(data+'3')]
        return self.wio_host

api.add_resource(PublicGetCurrentWeather, '/mood', '/mood/<current_mood>', endpoint='todo_ep')
