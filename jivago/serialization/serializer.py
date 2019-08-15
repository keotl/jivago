from typing import Union

from jivago.serialization.serialization_exception import SerializationException

BUILTIN_TYPES = (str, float, int, bool)


class Serializer(object):

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

        raise SerializationException(obj)
