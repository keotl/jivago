import anachronos

from e2e_test.runner import http


class CorsTests(anachronos.TestCase):

    def test_cors_headers_injected_on_success(self):
        res = http.get("/")

        self.assertEqual("http://jivago.io", res.headers["Access-Control-Allow-Origin"])
        self.assertEqual("*", res.headers["Access-Control-Allow-Headers"])
        self.assertEqual("*", res.headers["Access-Control-Allow-Methods"])

    def test_cors_headers_injected_on_error(self):
        res = http.get("/error")

        self.assertEqual("http://jivago.io", res.headers["Access-Control-Allow-Origin"])
        self.assertEqual("*", res.headers["Access-Control-Allow-Headers"])
        self.assertEqual("*", res.headers["Access-Control-Allow-Methods"])

    def test_cors_preflight_succeeds_for_allowed_origin(self):
        res = http.options("/", headers={"Origin": "http://jivago.io"})

        self.assertEqual(200, res.status_code)
        self.assertEqual("http://jivago.io", res.headers["Access-Control-Allow-Origin"])
        self.assertEqual("*", res.headers["Access-Control-Allow-Headers"])
        self.assertEqual("*", res.headers["Access-Control-Allow-Methods"])

    def test_cors_preflight_fails_on_missing_origin(self):
        res = http.options("/")

        self.assertEqual(400, res.status_code)
        self.assertEqual("http://jivago.io", res.headers["Access-Control-Allow-Origin"])
        self.assertEqual("*", res.headers["Access-Control-Allow-Headers"])
        self.assertEqual("*", res.headers["Access-Control-Allow-Methods"])

    def test_cors_preflight_fails_on_disallowed_origin(self):
        res = http.options("/", headers={"Origin": "http://hello.example.com"})

        self.assertEqual(400, res.status_code)
        self.assertEqual("http://jivago.io", res.headers["Access-Control-Allow-Origin"])
        self.assertEqual("*", res.headers["Access-Control-Allow-Headers"])
        self.assertEqual("*", res.headers["Access-Control-Allow-Methods"])

    def test_cors_preflight_fails_on_unknown_path(self):
        res = http.options("/foo/bar/unknown/path")

        self.assertEqual(404, res.status_code)


if __name__ == '__main__':
    anachronos.run_tests()
