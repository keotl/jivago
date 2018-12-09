def is_typing_meta_collection(clazz, metas=('List', 'Collection', 'Iterable', 'Tuple')) -> bool:
    if not hasattr(clazz, "__module__"):
        return False
    typing_meta_name = clazz._name if hasattr(clazz, "_name") else clazz.__name__ if hasattr(clazz, "__name__") else ""
    if typing_meta_name is None: # Python3.7 Union metas
        typing_meta_name = ""
    return clazz.__module__ == 'typing' and hasattr(clazz, '__args__') and typing_meta_name in metas


def is_union_typing_meta(clazz):
    return is_typing_meta_collection(clazz, ("",))

def is_optional_typing_meta(clazz):
    return is_union_typing_meta(clazz) and type(None) in clazz.__args__
