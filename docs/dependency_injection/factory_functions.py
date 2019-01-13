from jivago.inject.annotation import Provider


class DatabaseConnection(object):

    def __init__(self):
        # open a connection, etc.
        pass

    def query_database(self) -> int:
        # use the opened connection, etc.
        return 5


connection = None


@Provider
def get_database_connection() -> DatabaseConnection:
    global connection
    if connection is None:
        connection = DatabaseConnection()
    return connection
