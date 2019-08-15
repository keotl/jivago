from typing import Union

from jivago.lang.stream import Stream
from jivago.serialization.serialization.datetime_serialization_strategy import DatetimeSerializationStrategy
from jivago.serialization.serialization_exception import SerializationException

BUILTIN_TYPES = (str, float, int, bool)


class Serializer(object):

    def __init__(self):
        self.strategies = [DatetimeSerializationStrategy()]

    def serialize(self, obj: object) -> Union[dict, list]:
        if isinstance(obj, list) or isinstance(obj, tuple):
            return [self.serialize(x) for x in obj]

        if isinstance(obj, dict):
            dictionary = obj
            for key, value in dictionary.items():
                dictionary[key] = self.serialize(value)
            return dictionary
        if type(obj) in BUILTIN_TYPES:
            return obj

        if hasattr(obj, '__dict__'):
            return self.serialize(obj.__dict__)

        return Stream(self.strategies) \
            .firstMatch(lambda s: s.can_handle_serialization(obj)) \
            .map(lambda s: s.serialize(obj)) \
            .orElseThrow(SerializationException(f"Cannot serialize type {obj.__class__}. {obj}"))
