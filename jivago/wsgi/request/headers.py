from jivago.lang.stream import Stream


class Headers(object):

    def __init__(self, content=None):
        self.content = {} if content is None else Stream(content.items()).map(lambda key, value: (key.upper(), value)).toDict()

    def __setitem__(self, key: str, value: str):
        self.content[key.upper()] = value

    def __getitem__(self, item: str) -> str:
        return self.content.get(item.upper())

    def values(self):
        return self.content.values()

    def keys(self):
        return self.content.keys()

    def items(self):
        return self.content.items()
