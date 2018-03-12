import example_app
from jivago.application import JivagoApplication


class Application(object):

    def __init__(self):
        self.name = 5


if __name__ == '__main__':
    JivagoApplication(example_app)
    import jivago.inject.scope as scope
    print(scope.scoped_objects)
    print("hello")
