import os

basedir = os.path.abspath(os.path.dirname(__file__))

CACHE_STORAGE_TYPE = 'DATABASE'
DATABASE_NAME = 'db_cache'
DATABASE_PATH = os.path.join(basedir, DATABASE_NAME + '.db')

