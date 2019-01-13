from jivago.lang.annotations import Serializable


@Serializable
class RequestDto(object):
    name: str
    age: int


@Serializable
class AuthenticatedRequestDto(object):
    name: str
    role: str
