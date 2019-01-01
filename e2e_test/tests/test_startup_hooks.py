import anachronos
from anachronos.test.boot.test_runner import RunWith
from e2e_test.testing_messages import PREINIT, INIT, POSTINIT
from e2e_test.tests.runner import AppRunner


@RunWith(AppRunner)
class StartupHooksTest(anachronos.TestCase):

    def test_hook_order(self):
        self.assertThat(PREINIT).is_before(INIT)
        self.assertThat(INIT).is_before(POSTINIT)
        self.assertThat(POSTINIT).is_after(PREINIT)


if __name__ == '__main__':
    anachronos.run_tests()
