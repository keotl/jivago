from jivago.jivago_application import JivagoApplication
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET


@Resource("/")
class HelloResource(object):

    @GET
    def get_hello(self) -> str:
        return "Hello World!"


app = JivagoApplication()

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple('localhost', 4000, app)
