from typing import TypeVar, Type

from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.serialization.hooks.built_in_type_deserialization_object_hook import BuiltInTypeDeserializationObjectHook
from jivago.serialization.hooks.dictionary_deserialization_object_hook import DictionaryDeserializationObjectHook
from jivago.serialization.hooks.list_deserialization_hook import ListDeserializationHook
from jivago.serialization.hooks.optional_attribute_deserialization_hook import OptionalAttributeDeserializationHook
from jivago.serialization.hooks.registered_serializable_type_deserialization_hook import \
    RegisteredSerializableTypeDeserializationHook
from jivago.serialization.hooks.tuple_deserialization_hook import TupleDeserializationHook
from jivago.serialization.hooks.typed_dictionary_deserialization_hook import TypedDictionaryDeserializationHook
from jivago.serialization.hooks.typed_list_deserialization_hook import TypedListDeserializationHook
from jivago.serialization.hooks.typed_tuple_deserialization_hook import TypedTupleDeserializationHook
from jivago.wsgi.invocation.incorrect_attribute_type_exception import IncorrectAttributeTypeException

T = TypeVar('T')


class Deserializer(object):

    def __init__(self, registry: Registry):
        self.hooks = [
            BuiltInTypeDeserializationObjectHook(),
            RegisteredSerializableTypeDeserializationHook(registry, self),
            TypedDictionaryDeserializationHook(self),
            OptionalAttributeDeserializationHook(self),
            TypedListDeserializationHook(self),
            TypedTupleDeserializationHook(self),
            DictionaryDeserializationObjectHook(),
            ListDeserializationHook(),
            TupleDeserializationHook()
        ]

    def deserialize(self, obj: dict, object_clazz: Type[T]) -> T:
        try:
            return Stream(self.hooks). \
                firstMatch(lambda hook: hook.can_handle_deserialization(object_clazz)) \
                .deserialize(obj, object_clazz)
        except AttributeError:
            raise IncorrectAttributeTypeException()
