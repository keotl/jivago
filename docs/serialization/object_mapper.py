from jivago.serialization.object_mapper import ObjectMapper


class Dto(object):
    name: str


object_mapper = ObjectMapper()

dto: Dto = object_mapper.deserialize('{"name": "paul" }', Dto)

json_str = object_mapper.serialize(dto)
