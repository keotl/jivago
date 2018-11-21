from jivago.jivago_application import JivagoApplication

app = JivagoApplication()

if __name__ == '__main__':
    # using the bundled werkzeug server
    app.run_dev(port=4000, host="localhost")

    # or alternatively
    from werkzeug.serving import run_simple

    run_simple('localhost', 4000, app)
