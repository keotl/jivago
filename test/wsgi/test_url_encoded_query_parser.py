import unittest

from jivago.wsgi.request.url_encoded_query_parser import UrlEncodedQueryParser

A_METHOD = "GET"
A_PATH = "/hello"
HEADERS = {}
QUERY_STRING = "query=foobar&query2=barbaz"
BODY = ""


class UrlEncodedQueryParserTest(unittest.TestCase):

    def setUp(self):
        self.queryParser = UrlEncodedQueryParser()

    def test_whenParsingQueryParameters_thenReturnQueryKeyPairsInADictionary(self):
        parameters = self.queryParser.parse_urlencoded_query(QUERY_STRING)

        self.assertEqual(2, len(parameters))
        self.assertEqual("foobar", parameters['query'])
        self.assertEqual("barbaz", parameters['query2'])

    def test_givenRequestWithoutQueryParameters_whenParsingQueryParameters_thenReturnEmptyDictionary(self):
        parameters = self.queryParser.parse_urlencoded_query("")

        self.assertEqual(0, len(parameters))
