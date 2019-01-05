import anachronos

from e2e_test.runner import http
from e2e_test.testing_messages import SIMPLE_GET, SIMPLE_POST_DTO, DIFFERENT_POST_DTO


class SimpleResourceTest(anachronos.TestCase):

    def test_simple_get(self):
        http.get("/")

        self.assertThat(SIMPLE_GET).is_stored()

    def test_post_dto(self):
        response = http.post("/", json={'name': 'Paul Atreides', 'age': 17}).json()

        self.assertThat(SIMPLE_POST_DTO).is_stored()
        self.assertEqual('Paul Atreides', response['name'])

    def test_selectRightResourceMethodBasedOnPayloadDtoType(self):
        response = http.post("/", json={'name': 'Paul Atreides', 'age': 17, 'role': "foobar"}).json()

        self.assertThat(DIFFERENT_POST_DTO).is_stored()
        self.assertEqual('Paul Atreides', response['name'])


if __name__ == '__main__':
    anachronos.run_tests()

