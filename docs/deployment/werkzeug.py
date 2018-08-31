from jivago.jivago_application import JivagoApplication

app = JivagoApplication()

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple('localhost', 4000, app)
