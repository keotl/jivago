import unittest

from jivago.wsgi.invocation.parameter_selection.query_parameter_selector import QueryParameterSelector
from jivago.wsgi.invocation.parameters import QueryParam


class QueryParameterSelectorTest(unittest.TestCase):

    def setUp(self):
        self.selector = QueryParameterSelector()

    def test_whenMatchingFunction_thenMatchQueryParameterTypes(self):
        self.assertTrue(self.selector.matches(QueryParam[str]))
        self.assertFalse(self.selector.matches(str))
