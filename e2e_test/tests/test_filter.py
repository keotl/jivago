import anachronos

from e2e_test.runner import http
from e2e_test.testing_messages import FILTER


class FilterTest(anachronos.TestCase):

    def test_filterIsCalled(self):
        http.get("/")

        self.assertThat(FILTER).is_stored()


if __name__ == '__main__':
    anachronos.run_tests()
