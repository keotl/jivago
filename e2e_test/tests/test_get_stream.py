import time
from contextlib import closing

import anachronos
from anachronos.configuration import RunWith

from e2e_test.runner import GunicornRunner, http


@RunWith(GunicornRunner)
class GetStreamTest(anachronos.TestCase):
    def test_get_stream(self):
        with closing(http.get('/stream', stream=True)) as r:
            x = r.iter_content()
            content = b""
            for i in x:
                content += i

        self.assertEqual(r.status_code, 200)
        self.assertEqual(content.decode("utf-8"), "".join([x.decode("utf-8") for x in generate_bytes()]))


def generate_bytes():
    for i in range(0, 5):
        yield f"test-{i}\r\n".encode("utf-8")
        time.sleep(0.1)


if __name__ == '__main__':
    anachronos.run_tests()
