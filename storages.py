import sqlite3
import config


class Storage(object):
    def save(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass


class DatabaseStorage(Storage):
    def __init__(self):
        self.path = config.DATABASE_PATH

        if not self._exists():
            self._create_db()

        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def save(self, url_hash, headers, response):
        text = ''.join(response)
        self.cursor.execute("INSERT INTO cache VALUES(?, ?, ?)", (url_hash, headers, text))
        self.connection.commit()

    def load(self, url_hash):
        response = ''
        for row in self.cursor.execute("SELECT headers, response FROM cache WHERE url_hash=?", (url_hash,)):
            response = ''.join([response, row[0]])

        if not response:
            return []
        else:
            return [response]

    def _exists(self):
        import os
        return os.path.exists(self.path)

    def _create_db(self):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE cache (url_hash TEXT, headers TEXT, response TEXT)")
            connection.commit()


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
