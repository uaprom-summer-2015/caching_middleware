from util import controller, Response, Router
from random import randint

@controller
def index(request):
    return Response(200, str(randint(0, 100)))

@controller
def hello(request):
    name = request.GET.get('name', ["Anonymous"])[0]
    return Response(200, "Hello %s" % name)

router = Router({
    '/index': index,
    '/hello': hello,
})
