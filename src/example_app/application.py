import example_app
from jivago.application import JivagoApplication
from jivago.lang import annotations


class Application(object):

    def __init__(self):
        self.name = 5


if __name__ == '__main__':
    JivagoApplication(example_app)
    for i in annotations.Registry.components:
        item = i()
        print(item)
    print(annotations.Registry.components)

