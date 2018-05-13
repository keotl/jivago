from jivago.lang.stream import Stream


class UrlEncodedQueryParser(object):

    def parse_urlencoded_query(self, query_string: str) -> dict:
        pairs = query_string.split("&")
        return Stream(pairs).filter(lambda x: x != "").map(lambda pair: pair.split("=")).toDict()
