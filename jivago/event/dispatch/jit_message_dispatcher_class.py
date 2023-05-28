from typing import Callable
import logging
import traceback as tb

from jivago.event.dispatch.message_dispatcher_class import MessageDispatcherClass
from jivago.inject.service_locator import ServiceLocator


class JitMessageDispatcherClass(MessageDispatcherClass):

    def __init__(self, message_name: str, clazz: type, method: Callable, service_locator: ServiceLocator):
        super().__init__(message_name, method)
        self.method = method
        self.clazz = clazz
        self.service_locator = service_locator
        self._logger = logging.getLogger("MessageDispatcher")

    def handle(self, payload: object):
        try:
            instance = self.service_locator.get(self.clazz)
            if self._requires_payload_parameter():
                return self.method(instance, payload)
            return self.method(instance)
        except KeyboardInterrupt as e:
            raise e
        except Exception:
            self._logger.error(f"Unhandled exception while handling message {self.message_name}. {tb.format_exc()}")
            return None



