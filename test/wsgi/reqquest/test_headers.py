import unittest

from jivago.wsgi.request.headers import Headers


class HeadersTest(unittest.TestCase):

    def test_whenGettingHeaderValue_thenMatchRegardlessOfCase(self):
        headers = Headers({"Foo-Bar": "baz"})

        self.assertEqual("baz", headers['FOO_BAR'])
        self.assertEqual("baz", headers['Foo-Bar'])
        self.assertEqual("baz", headers['FOo-baR'])
