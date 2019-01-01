from jivago.lang.annotations import Serializable


@Serializable
class RequestDto(object):
    name: str
    age: int
