import anachronos

from e2e_test.runner import http
from e2e_test.testing_messages import SIMPLE_GET, SIMPLE_POST_DTO, DIFFERENT_POST_DTO, GET_WITH_PARAMETERS, \
    GET_WITH_PATH_PARAMETER


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

    def test_givenMissingOrMalformedPayloadDto_thenReturn400BadRequest(self):
        response = http.post("/", json={})

        self.assertEqual(400, response.status_code)

    def test_getWithQueryParameters(self):
        response = http.get("/params?query=foo&age=13")

        self.assertEqual(200, response.status_code)
        self.assertThat(GET_WITH_PARAMETERS).is_contained()

    def test_givenMissingOrMalformedQueryParams_thenReturn400BadRequest(self):
        response = http.get("/params?query=foo&age=a")

        self.assertEqual(400, response.status_code)
        self.assertThat(GET_WITH_PARAMETERS + " foo a").is_never_stored()

    def test_withPathParameter(self):
        http.get("/path/foobar")

        self.assertThat(GET_WITH_PATH_PARAMETER).is_contained()


if __name__ == '__main__':
    anachronos.run_tests()
