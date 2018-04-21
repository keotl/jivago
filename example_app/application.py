import example_app
from jivago.application import JivagoApplication


class Application(object):

    def __init__(self):
        self.name = 5


if __name__ == '__main__':
    app = JivagoApplication(example_app, debug=True)

    from werkzeug.serving import run_simple

    run_simple('localhost', 4000, app.router.route)
