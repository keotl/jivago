from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET


@Resource("/error")
class ErrorResource(object):

    @GET
    def raise_an_exception(self):
        raise NotImplementedError
