import anachronos

from e2e_test.testing_messages import BACKGROUND_WORKER


class BackgroundWorkerTest(anachronos.TestCase):

    def test_hook_order(self):
        self.assertThat(BACKGROUND_WORKER).is_stored()


if __name__ == '__main__':
    anachronos.run_tests()
