import time

import anachronos
from e2e_test.testing_messages import SCHEDULED


class ScheduledTasksTest(anachronos.TestCase):

    def test_scheduled_component_startup(self):
        time.sleep(2)
        self.assertThat(SCHEDULED).occurs_every(seconds=1)


if __name__ == '__main__':
    anachronos.run_tests()
