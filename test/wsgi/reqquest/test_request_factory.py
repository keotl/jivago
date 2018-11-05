import unittest

from jivago.wsgi.request.request_factory import RequestFactory


class RequestFactoryTest(unittest.TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_whenBuildingRequest_thenFormatCustomHttpHeadersUsingCamelCase(self):
        request = self.request_factory.build_request(WSGI_ENV)

        self.assertTrue(("Foo", "bar") in request.headers.items())

    def test_givenCustomHeaderWithUnderscores_whenBuildingRequest_thenReplaceUnderscoresWithHyphens(self):
        request = self.request_factory.build_request(WSGI_ENV)

        self.assertTrue(("Foo-Bar", "bar") in request.headers.items())

    def test_whenBuildingRequest_thenPopulateRequiredHeaderFields(self):
        request = self.request_factory.build_request(WSGI_ENV)

        self.assertEqual("GET", request.method)
        self.assertEqual("/", request.path)
        self.assertEqual("", request.queryString)

    def test_givenCustomHeaderStartingWithP_whenBuildingRequest_thenDoNotRemoveTheLeadingP(self):
        request = self.request_factory.build_request(WSGI_ENV)

        self.assertEqual("postman", request.headers['Postman-Token'])

    def test_givenJsonPost_whenBuildingRequest_thenAddContentTypeHeader(self):
        request = self.request_factory.build_request(POST_WSGI_ENV)

        self.assertEqual(b'{\n"message" : "string"\n}', request.body)
        self.assertEqual("application/json", request.headers['Content-Type'])


class DummyWsgiReadStream(object):
    def __init__(self, content=b""):
        self.content = content

    def read(self, *args):
        return self.content


WSGI_ENV = {
    'HTTP_FOO': 'bar',  # custom header
    'HTTP_FOO_BAR': 'bar',  # custom header
    'wsgi.version': (1, 0), 'wsgi.url_scheme': 'http', 'wsgi.input': DummyWsgiReadStream(), 'wsgi.errors': lambda x: x,
    'wsgi.multithread': False, 'wsgi.multiprocess': False, 'wsgi.run_once': False,
    'werkzeug.server.shutdown': lambda x: x,
    'SERVER_SOFTWARE': 'Werkzeug/0.14.1',
    'REQUEST_METHOD': 'GET',
    'SCRIPT_NAME': '',
    'PATH_INFO': '/',
    'QUERY_STRING': '',
    'HTTP_POSTMAN_TOKEN': "postman",
    'REMOTE_ADDR': '127.0.0.1', 'REMOTE_PORT': 58576,
    'SERVER_NAME': '127.0.0.1', 'SERVER_PORT': '4000',
    'SERVER_PROTOCOL': 'HTTP/1.1', 'HTTP_HOST': 'localhost:4000',
    'HTTP_CONNECTION': 'keep-alive',
    'HTTP_CACHE_CONTROL': 'no-cache',
    'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36',
    'HTTP_ACCEPT': '*/*', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br',
    'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.9,fr-CA;q=0.8,fr;q=0.7'}

POST_WSGI_ENV = {
    'CONTENT_TYPE': 'application/json',
    'wsgi.version': (1, 0), 'wsgi.url_scheme': 'http',
    'wsgi.input': DummyWsgiReadStream(b'{\n"message" : "string"\n}'),
    'wsgi.errors': lambda x: x,
    'wsgi.multithread': False,
    'wsgi.multiprocess': False,
    'wsgi.run_once': False,
    'werkzeug.server.shutdown': lambda x: x,
    'SERVER_SOFTWARE': 'Werkzeug/0.14.1', 'REQUEST_METHOD': 'POST',
    'SCRIPT_NAME': '', 'PATH_INFO': '/', 'QUERY_STRING': '', 'REMOTE_ADDR': '127.0.0.1',
    'REMOTE_PORT': 47858, 'SERVER_NAME': '127.0.0.1', 'SERVER_PORT': '4000',
    'SERVER_PROTOCOL': 'HTTP/1.1', 'HTTP_HOST': 'localhost:4000',
    'HTTP_CONNECTION': 'keep-alive', 'CONTENT_LENGTH': '24',
    'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36',
    'HTTP_CACHE_CONTROL': 'no-cache',
    'HTTP_ACCEPT': '*/*', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br',
    'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.9,fr-CA;q=0.8,fr;q=0.7'}
