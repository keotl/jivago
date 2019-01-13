from typing import List

from jivago.lang.stream import Stream


def split_path(path: str) -> List[str]:
    return Stream(path.split('/')).filter(lambda x: x != "").toList()
