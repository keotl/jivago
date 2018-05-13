from jinja2 import Template

from jivago.lang.annotations import Override, Inject
from jivago.templating.rendered_view import RenderedView
from jivago.templating.view_template_repository import ViewTemplateRepository
from jivago.wsgi.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class TemplateFilter(Filter):

    @Inject
    def __init__(self, view_template_repository: ViewTemplateRepository,
                 dto_serialization_handler: DtoSerializationHandler):
        self.dto_serialization_handler = dto_serialization_handler
        self.view_template_repository = view_template_repository

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        chain.doFilter(request, response)

        if isinstance(response.body, RenderedView):
            rendered_view = response.body
            template_text = self.view_template_repository.get_template(rendered_view.view_file)
            template_parameters = rendered_view.data
            if self.dto_serialization_handler.is_serializable(rendered_view.data.__class__):
                template_parameters = self.dto_serialization_handler.serialize(rendered_view.data)
            response.body = Template(template_text).render(**template_parameters)

            response.headers['Content-Type'] = "text/html"
