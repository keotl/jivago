from typing import TypeVar, Type

from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.serialization.deserialization.built_in_type_deserialization_strategy import \
    BuiltInTypeDeserializationStrategy
from jivago.serialization.deserialization.datetime_deserialization_strategy import DatetimeDeserializationStrategy
from jivago.serialization.deserialization.dictionary_deserialization_strategy import DictionaryDeserializationStrategy
from jivago.serialization.deserialization.list_deserialization_strategy import ListDeserializationStrategy
from jivago.serialization.deserialization.named_tuple_deserialization_strategy import NamedTupleDeserializationStrategy
from jivago.serialization.deserialization.optional_attribute_deserialization_strategy import \
    OptionalAttributeDeserializationStrategy
from jivago.serialization.deserialization.registered_serializable_type_deserialization_strategy import \
    RegisteredSerializableTypeDeserializationStrategy
from jivago.serialization.deserialization.tuple_deserialization_strategy import TupleDeserializationStrategy
from jivago.serialization.deserialization.typed_dictionary_deserialization_strategy import \
    TypedDictionaryDeserializationStrategy
from jivago.serialization.deserialization.typed_list_deserialization_strategy import TypedListDeserializationStrategy
from jivago.serialization.deserialization.typed_tuple_deserialization_strategy import TypedTupleDeserializationStrategy
from jivago.serialization.serialization_exception import SerializationException
from jivago.wsgi.invocation.incorrect_attribute_type_exception import IncorrectAttributeTypeException

T = TypeVar('T')


class Deserializer(object):

    def __init__(self, registry: Registry):
        self.deserialization_strategies = [
            BuiltInTypeDeserializationStrategy(),
            DatetimeDeserializationStrategy(),
            NamedTupleDeserializationStrategy(self),
            TypedDictionaryDeserializationStrategy(self),
            OptionalAttributeDeserializationStrategy(self),
            TypedListDeserializationStrategy(self),
            TypedTupleDeserializationStrategy(self),
            RegisteredSerializableTypeDeserializationStrategy(registry, self),
            DictionaryDeserializationStrategy(),
            ListDeserializationStrategy(),
            TupleDeserializationStrategy()
        ]

    def is_deserializable_type(self, object_clazz: type) -> bool:
        return Stream(self.deserialization_strategies) \
            .anyMatch(lambda s: s.can_handle_deserialization(object_clazz))

    def deserialize(self, obj: dict, object_clazz: Type[T]) -> T:
        try:
            return Stream(self.deserialization_strategies). \
                firstMatch(lambda s: s.can_handle_deserialization(object_clazz)) \
                .orElseThrow(SerializationException) \
                .deserialize(obj, object_clazz)
        except (AttributeError, TypeError):
            raise IncorrectAttributeTypeException()
