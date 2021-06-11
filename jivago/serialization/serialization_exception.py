class SerializationException(Exception):
    pass


class NoMatchingDeserializationStrategyException(SerializationException):
    def __init__(self, clazz: type):
        super().__init__(self,
                         f"Could not find an appropriate deserialization strategy for type {clazz}. Are you missing the '@Serializable' annotation?")
