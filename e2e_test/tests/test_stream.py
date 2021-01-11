import time

import anachronos

from e2e_test.runner import http
from e2e_test.testing_messages import POST_HTTP_STREAM


class StreamTest(anachronos.TestCase):

    def test_post_stream(self):
        res = http.post("/stream", data=generate_bytes())

        self.assertEqual(res.status_code, 200)
        self.assertThat(POST_HTTP_STREAM + f" {''.join([ x.decode('utf-8') for x in generate_bytes()])}")


def generate_bytes():
    for i in range(0, 5):
        yield f"test-{i}\r\n".encode("utf-8")
        time.sleep(0.1)
