import anachronos
from anachronos.test.boot.test_runner import RunWith
from e2e_test.testing_messages import SIMPLE_GET
from e2e_test.tests.runner import http, AppRunner


@RunWith(AppRunner)
class SimpleResourceTest(anachronos.TestCase):

    def test_simple_get(self):
        http.get("/")

        self.assertThat(SIMPLE_GET).is_stored()


if __name__ == '__main__':
    anachronos.run_tests()
