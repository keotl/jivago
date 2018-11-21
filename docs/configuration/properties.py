from jivago.config.properties.application_properties import ApplicationProperties
from jivago.lang.annotations import Inject
from jivago.lang.registry import Component


@Component
class MyComponent(object):

    @Inject
    def __init__(self, application_properties: ApplicationProperties):
        self.application_properties = application_properties

    def do_something(self):
        print(self.application_properties["my_property"])
