from pymodm import connect
import urllib 
import yaml
# from cryptography.fernet import Fernet
import sys
import os
from musicPlayer.config import config

user = config.DB_USER
password = config.DB_PASSWORD

MONGO_DB_NAME = config.DB_NAME
MONGO_DB_URL = config.DB_HOST
MONGOD_URI = 'mongodb://'+user+":"+password+"@"+MONGO_DB_URL+'/'+MONGO_DB_NAME 

# connect to mongo
connect(MONGOD_URI)
print('\nINFO: connected to {}'.format(MONGO_DB_NAME))