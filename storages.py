import os
import sqlite3
import config
from contextlib import contextmanager

class Storage(object):
    def save(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass


class DatabaseStorage(Storage):
    def __init__(self):
        if not os.path.exists(config.DATABASE_PATH):
            self.create_db(config.DATABASE_PATH)

        self.path = config.DATABASE_PATH
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def save(self, url_hash, response):
        text = ''.join(response)
        self.cursor.execute("INSERT INTO cache VALUES(?, ?)", (url_hash, text))
        self.connection.commit()

    def load(self, url_hash):
        response = ''
        for row in self.cursor.execute("SELECT response FROM cache WHERE url_hash=?", (url_hash,)):
            response = ''.join([response, row[0]])

        if not response:
            return []
        else:
            return [response]

    def exists(self, url_hash):
        result = self.cursor.execute('SELECT COUNT(*) FROM cache HAVING url_hash=?', (url_hash,))
        return False if result.rowcount == -1 else True

    @staticmethod
    def create_db(path):
        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE cache (url_hash TEXT, headers TEXT, response TEXT)")
            connection.commit()


@contextmanager
class SimpleCache(object):
    _storage_types = {
        'FILE': None,
        'DATABASE': DatabaseStorage,
        'MEMORY': None,
    }

    def __init__(self, storage_type_name):
        self.storage = self._storage_types[storage_type_name]()

    def save(self, url_hash, headers, response):
        self.storage.save(url_hash, headers, response)

    def load(self, url_hash):
        return self.storage.load(url_hash)
