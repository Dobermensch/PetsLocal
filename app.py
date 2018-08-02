import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig as devConfig

##lol = config.DevelopmentConfig()

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS', devConfig))
##app.config['APP_SETTINGS'] = devConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Pet, Customer, CustomerPreference


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()
