from flask import Flask, request
from time import strftime
import json, logging, sys
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from blueprints import app, manager

if __name__ == '__main__':

    formatter = logging.Formatter("[%(asctime)s]{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    log_handler = RotatingFileHandler("%s/%s" %(app.root_path, 'storage/log/app.log'), maxBytes = 10000000, backupCount = 10)
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)

    try:
        if sys.argv[1] == 'db':
            manager.run()
        else:
            app.run(debug = False, host = '0.0.0.0', port = 8000)
    except IndexError as e:
        app.run(debug = True, host = '0.0.0.0', port = 8000)

