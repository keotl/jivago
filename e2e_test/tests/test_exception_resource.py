import anachronos

from e2e_test.runner import http


class ExceptionResourceTest(anachronos.TestCase):

    def setUp(self):
        self.http = http.with_path("/error")

    def test_got500OnInternalServerError(self):
        response = self.http.get("")

        self.assertEqual(500, response.status_code)

    def test_got404OnResourceNotFound(self):
        response = self.http.get("/inexistent-path")

        self.assertEqual(404, response.status_code)

    def test_got405MethodNotAllowed(self):
        response = self.http.post("")

        self.assertEqual(405, response.status_code)


if __name__ == '__main__':
    anachronos.run_tests()
