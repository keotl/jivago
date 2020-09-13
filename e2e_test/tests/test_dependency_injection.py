import anachronos
import multiprocessing

from e2e_test.runner import http
from e2e_test.testing_messages import INSTANTIATED_LAZY_BEAN, INSTANTIATED_REQUEST_SCOPED_BEAN


class DependencyInjectionTest(anachronos.TestCase):

    def test_lazy_singleton_is_instantiated_once_and_only_once(self):
        res = http.get("/dependency/lazybean")
        http.get("/dependency/lazybean")

        self.assertEqual(200, res.status_code)
        self.assertThat(INSTANTIATED_LAZY_BEAN).is_stored_only_once()

    def test_request_scoped_component_is_instantiated_once_for_a_single_request(self):
        res = http.get("/dependency/request-scoped")

        self.assertEqual(200, res.status_code)
        self.assertThat(INSTANTIATED_REQUEST_SCOPED_BEAN + res.content.decode("utf-8")).is_stored_only_once()

    def test_request_scoped_components_are_not_shared_accross_requests(self):
        pool = multiprocessing.Pool(2)

        res = pool.map(do_test_request_scope_query, range(0, 2))

        self.assertFalse(res[0] == res[1])


def do_test_request_scope_query(_):
    res = http.get("/dependency/request-scoped")
    return res.content.decode("utf-8")


if __name__ == '__main__':
    anachronos.run_tests()
