''' Flask Configuration Settings File '''
import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    ''' Standard configuration settings for the flask app '''
    SECRET_KEY = config('SECRET_KEY')
    SQLACADEMY_TRACK_MODFICATIONS=config('SQLACADEMY_TRACK_MODFICATIONS',cast=bool)

class DevConfig(Config):
    ''' Developer configuration settings for the flask app '''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
    DEBUG = True
    SQLALCHEMY_ECHO = True
