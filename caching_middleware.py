from wsgiref.simple_server import make_server
from example_server import simple_app

import time

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

    def wrapped_app(environ, start_response):
        pathinfo = environ['PATH_INFO']
        querystr = environ['QUERY_STRING']
        if not pathinfo in _cache.iterkeys():
            _cache[pathinfo] = dict() 
        if (not querystr in _cache[pathinfo].iterkeys()) or (_cache[pathinfo][querystr]['timestamp'] + 3600 < now()):
            _cache[pathinfo][querystr] = get_data(environ, start_response)
        else:
            start_response(_cache[pathinfo][querystr]['status'], _cache[pathinfo][querystr]['headers'])
        print 'get_from_cache'
        return _cache[pathinfo][querystr]['response']

    return wrapped_app

if __name__ == '__main__':
    make_server('', 8000, cache(simple_app)).serve_forever()
