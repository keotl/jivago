import logging

import example_app
from jivago.jivago_application import JivagoApplication

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    app = JivagoApplication(example_app, debug=False)
    app.run_dev()
