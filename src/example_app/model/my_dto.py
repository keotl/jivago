from jivago.lang.annotations import Serializable


@Serializable
class MyDto(object):
    name: str
    age: int

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
