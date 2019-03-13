from jinja2 import Template

from jivago.lang.annotations import Override, Inject
from jivago.serialization.deserializer import Deserializer
from jivago.serialization.serializer import Serializer
from jivago.templating.rendered_view import RenderedView
from jivago.templating.view_template_repository import ViewTemplateRepository
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class TemplateFilter(Filter):

    @Inject
    def __init__(self, view_template_repository: ViewTemplateRepository,
                 serializer: Serializer, deserializer: Deserializer):
        self.deserializer = deserializer
        self.serializer = serializer
        self.view_template_repository = view_template_repository

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        chain.doFilter(request, response)

        if isinstance(response.body, RenderedView):
            rendered_view = response.body
            template_text = self.view_template_repository.get_template(rendered_view.view_file)
            template_parameters = rendered_view.data
            if self.deserializer.is_deserializable_type(rendered_view.data.__class__):
                template_parameters = self.serializer.serialize(rendered_view.data)
            response.body = Template(template_text).render(**template_parameters)

            response.headers['Content-Type'] = "text/html"
