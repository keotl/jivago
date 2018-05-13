import unittest
from unittest import mock

from jivago.templating.rendered_view import RenderedView
from jivago.templating.template_filter import TemplateFilter
from jivago.templating.view_template_repository import ViewTemplateRepository
from jivago.wsgi.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response

A_RESPONSE = Response.empty()

A_REQUEST = Request('GET', "/", {}, "", "")
A_TEMPLATE = "{{ foo }}"


class TemplateFilterTest(unittest.TestCase):

    def setUp(self):
        self.viewTemplateRepositoryMock: ViewTemplateRepository = mock.create_autospec(ViewTemplateRepository)
        self.serializationHandlerMock: DtoSerializationHandler = mock.create_autospec(DtoSerializationHandler)
        self.filterChainMock: FilterChain = mock.create_autospec(FilterChain)
        self.templateFilter = TemplateFilter(self.viewTemplateRepositoryMock, self.serializationHandlerMock)

    def test_givenAResponseWhichShouldNotBeTemplated_whenApplyingFilter_thenDoNothing(self):
        returned_response = Response.empty()

        self.templateFilter.doFilter(A_REQUEST, returned_response, self.filterChainMock)

        self.assertEqual(A_RESPONSE.headers.items(), returned_response.headers.items())
        self.assertEqual(A_RESPONSE.body, returned_response.body)
        self.assertEqual(A_RESPONSE.status, returned_response.status)

    def test_givenATemplatedResponse_whenApplyingFilter_thenContentTypeIsSetToTextHtml(self):
        a_templated_response = Response(200, {}, RenderedView("test.html", {"foo": "bar"}))
        self.viewTemplateRepositoryMock.get_template.return_value = A_TEMPLATE

        self.templateFilter.doFilter(A_REQUEST, a_templated_response, self.filterChainMock)

        self.assertEqual("text/html", a_templated_response.headers['Content-Type'])

    def test_givenATemplatedResponse_whenApplyingFilter_thenTheTemplateIsProcessedByJinja2(self):
        a_templated_response = Response(200, {}, RenderedView("test.html", {"foo": "bar"}))
        self.serializationHandlerMock.is_serializable.return_value = False
        self.viewTemplateRepositoryMock.get_template.return_value = A_TEMPLATE

        self.templateFilter.doFilter(A_REQUEST, a_templated_response, self.filterChainMock)

        self.assertEqual("bar", a_templated_response.body)

    def test_givenADto_whenApplyingFilter_thenDtoIsSerializedToDictionaryBeforeRenderingTheTemplate(self):
        A_DTO = object()
        a_templated_response = Response(200, {}, RenderedView("test.html", A_DTO))
        self.serializationHandlerMock.is_serializable.return_value = True
        self.serializationHandlerMock.serialize.return_value = {"foo": "bar"}
        self.viewTemplateRepositoryMock.get_template.return_value = A_TEMPLATE

        self.templateFilter.doFilter(A_REQUEST, a_templated_response, self.filterChainMock)

        self.assertEqual("bar", a_templated_response.body)
