from wsgiref.simple_server import make_server
from example_server import simple_app

import time

TIMEOUT = 30


def cache(app, _cache=dict()):

    def now():
        return time.time()

    def get_data(environ, start_response):
        data = dict()
        data['timestamp'] = now()
        data['response'] = app(environ, start_response)
        data['headers'] = start_response.im_self.headers._headers
        data['status'] = start_response.im_self.status
        return data

    def is_cache_expired(key):
        return _cache[key]['timestamp'] + TIMEOUT < now()

    def wrapped_app(environ, start_response):
        key = environ['PATH_INFO'] + '?' + environ['QUERY_STRING']
        if (key not in _cache.iterkeys()) or is_cache_expired(key):
            _cache[key] = get_data(environ, start_response)
        else:
            start_response(_cache[key]['status'], _cache[key]['headers'])
        return _cache[key]['response']

    return wrapped_app

if __name__ == '__main__':
    make_server('', 8000, cache(simple_app)).serve_forever()
