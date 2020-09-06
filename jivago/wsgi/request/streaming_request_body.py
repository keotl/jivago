import io


class StreamingRequestBody(object):

    def __init__(self, content: io.RawIOBase):
        self.content = content

    def read(self, n: int = 1) -> bytes:
        return self.content.read(n)

    def readall(self) -> bytes:
        return self.content.readall()

    def readinto(self, out: bytearray) -> int:
        return self.content.readinto(out)
