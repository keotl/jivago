from jivago.lang.stream import Stream


class Headers(object):

    def __init__(self, content=None):
        self.content = {} if content is None else content

    def __setitem__(self, key: str, value: str):
        self.content[key] = value

    def __getitem__(self, item: str) -> str:
        found_header = Stream(self.content.items()).firstMatch(
            lambda key, value: key == item or _format_camel_case(key) == _format_camel_case(item))
        if found_header:
            return found_header.get()[1]
        return None

    def values(self):
        return self.content.values()

    def keys(self):
        return self.content.keys()

    def items(self):
        return self.content.items()

    def __contains__(self, item):
        return _format_camel_case(item) in self.content


def _format_camel_case(message: str) -> str:
    return message.replace("_", "-").title()
