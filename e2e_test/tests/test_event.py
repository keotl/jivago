import anachronos

from e2e_test.runner import http
from e2e_test.testing_messages import RUNNABLE_EVENT_HANDLER, INSTANTIATED_EVENT_HANDLER, FUNCTION_EVENT_HANDLER


class EventTest(anachronos.TestCase):

    def test_sendEvent(self):
        http.get("/event")

        self.assertThat(RUNNABLE_EVENT_HANDLER).is_stored()
        self.assertThat(INSTANTIATED_EVENT_HANDLER).is_stored()
        self.assertThat(FUNCTION_EVENT_HANDLER).is_stored()


if __name__ == '__main__':
    anachronos.run_tests()
