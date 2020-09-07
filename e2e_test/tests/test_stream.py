from contextlib import closing

import anachronos
import time

from e2e_test.runner import http
from e2e_test.testing_messages import POST_HTTP_STREAM


class StreamTest(anachronos.TestCase):

    def test_post_stream(self):
        res = http.post("/stream", data=generate_bytes())

        self.assertEqual(res.status_code, 200)
        self.assertThat(POST_HTTP_STREAM + f" {''.join([ x.decode('utf-8') for x in generate_bytes()])}")

    def test_get_stream(self):
        with closing(http.get('/stream', stream=True)) as r:
            x = r.iter_content()
            for i in x:
                print(i)

        self.assertEqual(r.status_code, 200)


def generate_bytes():
    for i in range(0, 5):
        yield f"test-{i}".encode("utf-8")
        time.sleep(0.1)


if __name__ == '__main__':
    anachronos.run_tests()
