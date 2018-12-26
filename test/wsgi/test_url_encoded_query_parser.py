import unittest

from jivago.wsgi.invocation.url_encoded_form_parser import parse_urlencoded_form

A_METHOD = "GET"
A_PATH = "/hello"
HEADERS = {}
QUERY_STRING = "query=foobar&query2=barbaz"
BODY = ""


class UrlEncodedQueryParserTest(unittest.TestCase):

    def test_whenParsingQueryParameters_thenReturnQueryKeyPairsInADictionary(self):
        parameters = parse_urlencoded_form(QUERY_STRING)

        self.assertEqual(2, len(parameters))
        self.assertEqual("foobar", parameters['query'])
        self.assertEqual("barbaz", parameters['query2'])

    def test_givenRequestWithoutQueryParameters_whenParsingQueryParameters_thenReturnEmptyDictionary(self):
        parameters = parse_urlencoded_form("")

        self.assertEqual(0, len(parameters))
