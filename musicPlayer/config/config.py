import os
from os.path import join, dirname, realpath
from cryptography.fernet import Fernet


SECRET_KEY = Fernet.generate_key()
DEBUG = True
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_NAME = 'Flask-Music'
SESSION_TYPE = 'filesystem'
# SECRET_KEY = '12345678'