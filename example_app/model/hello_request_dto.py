from jivago.lang.annotations import Serializable


@Serializable
class HelloRequestDto(object):
    name: str
