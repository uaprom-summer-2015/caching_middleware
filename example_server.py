from wsgiref.simple_server import make_server
import time


def simple_app(environ, start_response):
    time.sleep(5)
    start_response( '200 OK', [('Content-type', 'text/plain')])
    return  ["Hello world"]

if __name__ == '__main__':
    make_server('', 8000, simple_app).serve_forever()
