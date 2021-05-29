from typing import Union, Iterable

from jivago.lang.stream import Stream
from jivago.serialization.serialization.datetime_serialization_strategy import DatetimeSerializationStrategy
from jivago.serialization.serialization.namedtuple_serialization_strategy import NamedTupleSerializationStrategy
from jivago.serialization.serialization_exception import SerializationException
from jivago.serialization.serialization_strategy import SerializationStrategy

BUILTIN_TYPES = (str, float, int, bool)


class Serializer(object):

    def __init__(self, additional_strategies: Iterable[SerializationStrategy] = ()):
        self.strategies = [*additional_strategies,
                           DatetimeSerializationStrategy(),
                           NamedTupleSerializationStrategy(self)]

    def serialize(self, obj: object) -> Union[dict, list]:
        res = Stream(self.strategies) \
            .firstMatch(lambda s: s.can_handle_serialization(obj)) \
            .map(lambda s: s.serialize(obj))

        if res.isPresent():
            return res.get()

        if obj is None:
            return None

        if issubclass(type(obj), BUILTIN_TYPES):
            return obj

        if isinstance(obj, list) or isinstance(obj, tuple):
            return [self.serialize(x) for x in obj]

        if isinstance(obj, dict):
            dictionary = obj
            for key, value in dictionary.items():
                dictionary[key] = self.serialize(value)
            return dictionary

        if hasattr(obj, '__dict__'):
            return self.serialize({**obj.__dict__})

        raise SerializationException(f"Cannot serialize type {obj.__class__}. {obj}")
