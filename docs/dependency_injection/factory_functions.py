from jivago.inject.annotation import Provider, Singleton


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


@Provider
@Singleton
def get_singleton_bean(my_dependency: Dependency) -> MySingletonBean:
    # Will only be called once
    return Dependency(...)
