from datetime import datetime
from typing import Optional

from jivago.lang.registry import ParametrizedAnnotation


@ParametrizedAnnotation
def Scheduled(cron: Optional[str], every: Optional[int], start: Optional[datetime]):
    return lambda x: x


class Duration(object):
    SECOND = object()
    MINUTE = object()
    HOUR = object()
    DAY = object()
    WEEK = object()
    MONTH = object()
    YEAR = object()
