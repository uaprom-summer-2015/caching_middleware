# coding=utf-8
from wsgiref.simple_server import make_server
from example_server import simple_app
def reverse_middleware(app):
    def wrapped_app(environ, start_response):
        response = app(environ, start_response)
        return [s[::-1] for s in response]
    return wrapped_app


def cache_middleware(app, cache=dict()):

    def _start_response(func, _headers_store):
        """Decorator for saving headers in _headers_store"""
        def wrapper(*args, **kwargs):
            _headers_store.append((args, kwargs))
            return func(*args, **kwargs)
        return wrapper

    def wrapper(environ, start_response):
        if environ['PATH_INFO'] in cache.iterkeys():
            args, kwargs = cache[environ['PATH_INFO']][0]  # Получаем все переданные headers из прошлого реквеста..
            start_response(*args, **kwargs)  # ..и отправляем их
            return cache[environ['PATH_INFO']][1]  # отправка тела
        else:
            _headers = list()  # делаем хранилище для хидеров
            # вызываем view'шку, передавая environ  и декоратор для start_response. Тело сохраняем в response,
            # хидеры - в _headers
            response = app(environ, _start_response(start_response, _headers))
            cache[environ['PATH_INFO']] = _headers.pop(), response  # сохраняем хидеры и тело в хэш
            return response

    return wrapper
#
if __name__ == '__main__':
    make_server('', 8000, cache_middleware(simple_app)).serve_forever()
