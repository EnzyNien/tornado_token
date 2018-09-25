import os

DEBUG = True

DB_PATH = 'postgresql://postgres:1234@127.0.0.1:5432/postgres'

SERVER_SCHEMA = 'http'
SERVER_HOST = u'127.0.0.1'
SERVER_PORT = 8001

SERVER_URL = '{}://{}:{}'.format(SERVER_SCHEMA, SERVER_HOST, SERVER_PORT)
