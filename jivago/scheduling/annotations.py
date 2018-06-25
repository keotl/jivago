from datetime import datetime
from typing import Optional

from jivago.lang.registry import ParametrizedAnnotation


@ParametrizedAnnotation
def Scheduled(cron: Optional[str], every: Optional["Duration"], start: Optional[datetime]):
    return lambda x: x


class _Interval(object):

    def __init__(self, interval_time_in_seconds: int):
        self.interval_time_in_seconds = interval_time_in_seconds


class Duration(object):
    SECOND = _Interval(1)
    MINUTE = _Interval(60)
    HOUR = _Interval(3600)
    DAY = _Interval(86400)
