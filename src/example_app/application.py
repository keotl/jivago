import example_app
from example_app.comp.beans import SomeOtherBean
from jivago.application import JivagoApplication


class Application(object):

    def __init__(self):
        self.name = 5


if __name__ == '__main__':
    app = JivagoApplication(example_app)

    bean = app.serviceLocator.get(SomeOtherBean)
    bean2 = app.serviceLocator.get(SomeOtherBean)

    assert bean == bean2
