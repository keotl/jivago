from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET


@Resource("/error")
class ErrorResource(object):

    @GET
    def raise_an_exception(self):
        raise NotImplementedError

    @GET
    @Path("/none")
    def null_pointer(self):
        return None.foo()
