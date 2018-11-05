from jivago.lang.stream import Stream
from jivago.wsgi.request.request import Request


class RequestFactory(object):

    def build_request(self, env: dict) -> Request:
        """Builds the Jivago request object from the WSGI environment dictionary."""
        raw_headers = Stream(env.items()).filter(lambda key, value: key.startswith("HTTP")).map(
            lambda key, value: (key.strip("HTTP_").title().replace("_", "-"), value)
        ).toDict()

        return Request("GET", "/", raw_headers, "", "")
