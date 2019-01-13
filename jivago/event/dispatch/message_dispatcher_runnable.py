from jivago.event.dispatch.jit_message_dispatcher_class import JitMessageDispatcherClass
from jivago.inject.service_locator import ServiceLocator


class MessageDispatcherRunnable(JitMessageDispatcherClass):

    def __init__(self, message_name: str, clazz: type, service_locator: ServiceLocator):
        super().__init__(message_name, clazz, clazz.run, service_locator)
