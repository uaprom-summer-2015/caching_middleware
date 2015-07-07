import config
from storages import SimpleCache


class CacheMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def wrapped_start_response(status, response_headers):
            headers.extend((status, response_headers))
            return start_response(status, response_headers)

        with SimpleCache(config.CACHE_STORAGE_TYPE) as cache:
            url_hash = hash(environ['PATH_INFO'] + '?' + environ['QUERY_STRING'])
            headers = []

            if cache.exists(url_hash):
                (status, response_headers), response = cache.load(url_hash)
                start_response(status, response_headers)
            else:
                response = self.app(environ, wrapped_start_response)
                cache.save(url_hash, headers, response)

            return response
