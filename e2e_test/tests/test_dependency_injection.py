import anachronos

from e2e_test.runner import http
from e2e_test.testing_messages import INSTANTIATED_LAZY_BEAN


class DependencyInjectionTest(anachronos.TestCase):

    def test_lazy_singleton_is_instantiated_once_and_only_once(self):
        res = http.get("/dependency/lazybean")
        http.get("/dependency/lazybean")

        self.assertEqual(200, res.status_code)
        self.assertThat(INSTANTIATED_LAZY_BEAN).is_stored_only_once()


if __name__ == '__main__':
    anachronos.run_tests()
