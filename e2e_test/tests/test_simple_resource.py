import anachronos
from e2e_test.testing_messages import SIMPLE_GET
from e2e_test.tests.runner import http


class SimpleResourceTest(anachronos.TestCase):

    def test_simple_get(self):
        http.get("/")

        self.assertThat(SIMPLE_GET).is_stored()

    def test_post_dto(self):
        response = http.post("/", json={'name': 'Paul Atreides', 'age': 17}).json()

        self.assertEqual('Paul Atreides', response['name'])


if __name__ == '__main__':
    anachronos.run_tests()
