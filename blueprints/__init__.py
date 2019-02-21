# app.py
from flask import Flask, request
import json
import logging
from flask_restful import Resource, Api, reqparse
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
api = Api(app, catch_all_404s=True)

app.config['JWT_SECRET_KEY'] = 'AdalahSebuahDosaJikaDurhaka'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@127.0.0.1:3306/rest_api'
app.config['APP_DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#middlewares
@app.after_request
def after_request(response):
    if request.method == 'GET':
        app.logger.error("REQUEST_LOG\t%s %s", json.dumps({'request': request.args.to_dict(
        ), 'response': json.loads(response.data.decode('utf-8'))}), response.status_code)
    else:
        app.logger.error("REQUEST_LOG\t%s %s", json.dumps(
            {'request': request.get_json(), 'response': json.loads(response.data.decode('utf-8'))}),response.status_code)
    return response

from blueprints.RequestExt.resources import bp_weather

app.register_blueprint(bp_weather)

db.create_all()