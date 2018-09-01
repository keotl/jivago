import example_app
from jivago.jivago_application import JivagoApplication


class Application(object):

    def __init__(self):
        self.name = 5


if __name__ == '__main__':
    app = JivagoApplication(example_app, debug=True)
    app.run_dev()
