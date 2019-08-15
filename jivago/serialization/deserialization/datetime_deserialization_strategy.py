from datetime import datetime, date
from typing import Type

import dateutil.parser

from jivago.lang.annotations import Override
from jivago.serialization.deserialization_strategy import DeserializationStrategy, T


class DatetimeDeserializationStrategy(DeserializationStrategy):

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return declared_type == datetime or declared_type == date

    @Override
    def deserialize(self, obj, declared_type: Type[T]) -> T:
        parsed_date = dateutil.parser.parse(obj)
        if declared_type == date:
            return parsed_date.date()
        return parsed_date
