from time import time, ctime

cache = {}
time_to_update = 10

def caching(app):

    def _start_response(func, _headers):
        def wrapper(*args, **kwargs):
            _headers.append((args, kwargs))
            return func(*args, **kwargs)
        return wrapper

    def wrapped_app(env, start_response):
        path = env['PATH_INFO']
        query = env['QUERY_STRING']
        method = env['REQUEST_METHOD']
        if method == 'GET' and path in cache:
            querys = cache[path]
            if query in querys:
                t, response, _headers = querys[query]
                if time() - t < time_to_update:
                    args, kwargs = _headers[0]
                    start_response(*args, **kwargs)
                    return response

        _headers = []
        response = app(env, _start_response(start_response, _headers))

        cache.setdefault(path,{}).setdefault(query, {})
        cache[path][query] = (time(), response, _headers)
        return response
    return wrapped_app


@caching
def simple_app(environ, start_response):
    start_response( '200 OK', [('Content-type', 'text/plain')])
    t = ctime()
    return 'path = %s?\nquery = %s\ntime = %s' % (environ['PATH_INFO'], environ['QUERY_STRING'], t)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 8000, simple_app).serve_forever()