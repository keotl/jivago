from jivago.lang.annotations import Serializable


@Serializable
class RequestDto(object):
    name: str
    age: int


@Serializable
class AuthenticatedRequestDto(RequestDto):
    role: str