from jivago.config.properties.application_properties import ApplicationProperties
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject


@Component
class MyComponent(object):

    @Inject
    def __init__(self, application_properties: ApplicationProperties):
        self.application_properties = application_properties

    def do_something(self):
        print(self.application_properties["my_property"])
