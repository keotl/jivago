from datetime import datetime, date

from jivago.lang.annotations import Override
from jivago.serialization.serialization_strategy import SerializationStrategy


class DatetimeSerializationStrategy(SerializationStrategy):

    @Override
    def can_handle_serialization(self, obj) -> bool:
        return isinstance(obj, datetime) or isinstance(obj, date)

    @Override
    def serialize(self, obj) -> object:
        return str(obj)
