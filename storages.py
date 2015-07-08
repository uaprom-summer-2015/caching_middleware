import sqlite3
import config


class Storage(object):
    def save(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass


class DatabaseStorage(Storage):
    def __init__(self):
        self.connection = sqlite3.connect(config.DATABASE_NAME + '.db')
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


class SimpleCache(object):
    __storage_types = {
        'FILE': None,
        'DATABASE': DatabaseStorage,
        'MEMORY': None,
    }

    def __init__(self, storage_type_name):
        self.storage = self.__storage_types[storage_type_name]()

    def save(self, url_hash, response):
        self.storage.save(url_hash, response)

    def load(self, url_hash):
        return self.storage.load(url_hash)
