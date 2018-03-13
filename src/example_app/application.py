import example_app
from jivago.application import JivagoApplication


class Application(object):

    def __init__(self):
        self.name = 5


if __name__ == '__main__':
    app = JivagoApplication(example_app)

    import jivago.inject.registry as registry

    component_ = registry.Registry.content[registry.Component]
    print(component_)
    print(app.get_annotated(registry.Component))
