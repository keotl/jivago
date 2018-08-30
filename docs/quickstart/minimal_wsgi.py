import my_hello_world_application
from jivago.jivago_application import JivagoApplication

app = JivagoApplication(my_hello_world_application)

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple('localhost', 4000, app)
