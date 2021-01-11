import unittest

from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.streaming_request_body_parameter_selector import \
    StreamingRequestBodyParameterSelector
from jivago.wsgi.request.streaming_request_body import StreamingRequestBody
from test_utils.request_builder import RequestBuilder


class StreamingRequestBodyParameterSelectorTest(unittest.TestCase):

    def setUp(self):
        self.selector = StreamingRequestBodyParameterSelector()

    def test_shouldMatchStreamingRequestBodyType(self):
        matches = self.selector.matches(StreamingRequestBody)

        self.assertTrue(matches)

    def test_givenStreamingRequestBody_whenFormattingParameter_thenReturnResponseBody(self):
        body = StreamingRequestBody("dummy")
        request = RequestBuilder().body(body).build()

        parameter = self.selector.format_parameter("param name", StreamingRequestBody, request)

        self.assertEqual(body, parameter)

    def test_givenIncorrectRequestBody_whenFormattingParameter_thenRaiseException(self):
        request = RequestBuilder().build()

        with self.assertRaises(MissingRouteInvocationArgument):
            self.selector.format_parameter("param name", StreamingRequestBody, request)
