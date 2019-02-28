from typing import TypeVar, Type

from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.serialization.hooks.built_in_type_deserialization_object_hook import BuiltInTypeDeserializationObjectHook
from jivago.serialization.hooks.dictionary_deserialization_object_hook import DictionaryDeserializationObjectHook
from jivago.serialization.hooks.registered_serializable_type_deserialization_hook import \
    RegisteredSerializableTypeDeserializationHook

T = TypeVar('T')


class Deserializer(object):

    def __init__(self, registry: Registry):
        self.hooks = [
            BuiltInTypeDeserializationObjectHook(),
            RegisteredSerializableTypeDeserializationHook(registry, self),
            DictionaryDeserializationObjectHook()
        ]

    def deserialize(self, obj: dict, object_clazz: Type[T]) -> T:
        return Stream(self.hooks). \
            firstMatch(lambda hook: hook.can_handle_deserialization(object_clazz)) \
            .deserialize(obj, object_clazz)
