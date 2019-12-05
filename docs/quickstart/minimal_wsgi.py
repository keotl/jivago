import my_hello_world_application
from jivago.jivago_application import JivagoApplication

app = JivagoApplication(my_hello_world_application)

if __name__ == '__main__':
    app.run_dev()
