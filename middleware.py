import config
from storages import SimpleCache


class CacheMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def wrapped_start_response(status, headers):
            response_headers.extend(headers)
            return start_response(status, response)

        url_query = environ['PATH_INFO'] + '?' + environ['QUERY_STRING']
        response_headers = []

        cache = SimpleCache(config.CACHE_STORAGE_TYPE)
        cached = cache.load(hash(url_query))

        if not cached:
            response = self.app(environ, wrapped_start_response)
            cache.save(hash(url_query), response_headers, response)
        else:
            response = cached

        return response
