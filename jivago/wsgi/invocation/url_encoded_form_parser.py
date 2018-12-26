from jivago.lang.stream import Stream


def parse_urlencoded_form(query_string: str) -> dict:
    pairs = query_string.split("&")
    return Stream(pairs).filter(lambda x: x != "").map(lambda pair: pair.split("=")).toDict()
