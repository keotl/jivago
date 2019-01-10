import os

import anachronos

from e2e_test.app import static
from e2e_test.runner import http


class StaticFilesTest(anachronos.TestCase):

    def setUp(self):
        self.http = http.with_path("/static")

    def test_serve_static_file(self):
        expected_content = open(os.path.join(os.path.dirname(static.__file__), "foo.txt"), 'rb').read()

        response = self.http.get("/foo.txt")

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_content, response.content)


if __name__ == '__main__':
    anachronos.run_tests()
