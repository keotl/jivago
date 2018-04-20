import unittest

from jivago.wsgi.request import Request

A_METHOD = "GET"
A_PATH = "/hello"
HEADERS = {}
QUERY_STRING = "query=foobar&query2=barbaz"
BODY = ""


class RequestTest(unittest.TestCase):

    def setUp(self):
        self.request = Request(A_METHOD, A_PATH, HEADERS, QUERY_STRING, BODY)

    def test_whenParsingQueryParameters_thenReturnQueryKeyPairsInADictionary(self):
        parameters = self.request.parse_query_parameters()

        self.assertEqual(2, len(parameters))
        self.assertEqual("foobar", parameters['query'])
        self.assertEqual("barbaz", parameters['query2'])

    def test_givenRequestWithoutQueryParameters_whenParsingQueryParameters_thenReturnEmptyDictionary(self):
        self.request.queryString = ""

        parameters = self.request.parse_query_parameters()

        self.assertEqual(0, len(parameters))
