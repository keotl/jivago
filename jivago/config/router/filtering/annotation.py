from typing import Type

from jivago.lang.registry import Annotation
from jivago.wsgi.filter.filter import Filter


@Annotation
def RequestFilter(filter_class: Type[Filter]):
    return filter_class
