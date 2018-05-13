from jivago.templating.rendered_view import RenderedView
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET


@Resource("/template")
class TemplatedResource(object):

    @GET
    def get(self) -> RenderedView:
        return RenderedView("template.html", {"name": "john"})
