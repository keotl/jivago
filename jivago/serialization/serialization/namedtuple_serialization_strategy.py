import sys

from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.serialization.serialization_strategy import SerializationStrategy


class NamedTupleSerializationStrategy(SerializationStrategy):

    def __init__(self, serializer: "Serializer"):
        self.serializer = serializer

    @Override
    def can_handle_serialization(self, obj) -> bool:
        declared_type = type(obj)
        if sys.version_info[0:2] == (3, 6):
            return hasattr(declared_type, "__bases__") \
                   and tuple in declared_type.__bases__ \
                   and hasattr(declared_type, "_field_types")

        return hasattr(declared_type, "__bases__") and tuple in declared_type.__bases__

    @Override
    def serialize(self, obj) -> object:
        return Stream(type(obj).__annotations__)\
            .map(lambda k: (k, self.serializer.serialize(obj.__getattribute__(k)))) \
            .toDict()
