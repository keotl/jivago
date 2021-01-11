import anachronos

from e2e_test.runner import http
from e2e_test.testing_messages import RUNNABLE_EVENT_HANDLER, INSTANTIATED_EVENT_HANDLER, FUNCTION_EVENT_HANDLER, \
    ASYNC_FUNCTION_EVENT_HANDLER, ASYNC_INSTANTIATED_EVENT_HANDLER, ASYNC_RUNNABLE_EVENT_HANDLER


class EventTest(anachronos.TestCase):

    def test_sendEvent(self):
        http.post("/event")

        self.assertThat(RUNNABLE_EVENT_HANDLER).is_stored()
        self.assertThat(INSTANTIATED_EVENT_HANDLER).is_stored()
        self.assertThat(FUNCTION_EVENT_HANDLER).is_stored()

    def test_sendAsyncEvent(self):
        http.post("/event/async")

        self.assertThat(ASYNC_RUNNABLE_EVENT_HANDLER).is_stored()
        self.assertThat(ASYNC_INSTANTIATED_EVENT_HANDLER).is_stored()
        self.assertThat(ASYNC_FUNCTION_EVENT_HANDLER).is_stored()


if __name__ == '__main__':
    anachronos.run_tests()
