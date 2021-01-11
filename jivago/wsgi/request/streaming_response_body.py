from typing import Iterable


class StreamingResponseBody(object):

    def __init__(self, iterable: Iterable[bytes]):
        self.iterable = iterable
