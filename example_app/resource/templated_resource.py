from example_app.model.hello_request_dto import HelloRequestDto
from jivago.templating.rendered_view import RenderedView
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET, POST


@Resource("/template")
class TemplatedResource(object):

    @GET
    def get(self) -> RenderedView:
        return RenderedView("template.html", {"name": "john"})

    @POST
    def post_form(self, hello_request: HelloRequestDto) -> RenderedView:
        return RenderedView("template.html", hello_request)
