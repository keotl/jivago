import example_app
from jivago.jivago_application import JivagoApplication

if __name__ == '__main__':
    app = JivagoApplication(example_app, debug=True)
    app.run_dev()
