from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET


@Resource("/")
class HelloResource(object):

    @GET
    def get_hello(self) -> str:
        return "Hello World!"
