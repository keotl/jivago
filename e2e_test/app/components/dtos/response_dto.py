from jivago.lang.annotations import Serializable


@Serializable
class ResponseDto(object):
    name: str
    allowed: bool

    def __init__(self, name: str, allowed: bool):
        self.name = name
        self.allowed = allowed
