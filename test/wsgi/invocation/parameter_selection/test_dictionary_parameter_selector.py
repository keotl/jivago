import unittest

from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.dictionary_parameter_selector import DictionaryParameterSelector
from test_utils.request_builder import RequestBuilder


class DictionaryParameterSelectorTest(unittest.TestCase):

    def setUp(self):
        self.parameter_selector = DictionaryParameterSelector()

    def test_givenStringRequestBody_whenGettingParameter_thenRaiseMissingRouteInvocationArgumentException(self):
        with self.assertRaises(MissingRouteInvocationArgument):
            self.parameter_selector.format_parameter("body", dict, RequestBuilder().build())
