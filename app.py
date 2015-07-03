from wsgiref.simple_server import make_server
from example_middleware import cache_middleware

from views import router

make_server('', 8000, cache_middleware(router)).serve_forever()
