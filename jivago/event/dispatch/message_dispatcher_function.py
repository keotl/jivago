from typing import Callable
import logging
import traceback as tb

from jivago.event.dispatch.message_dispatcher import MessageDispatcher
from jivago.lang.annotations import Override


class MessageDispatcherFunction(MessageDispatcher):

    def __init__(self, message_name: str, function: Callable):
        super().__init__(message_name)
        self.function = function
        self._logger = logging.getLogger("MessageDispatcher")

    @Override
    def handle(self, payload: object):
        if self._requires_payload_parameter():
            try:
                return self.function(payload)
            except KeyboardInterrupt as e:
                raise e
            except Exception:
                self._logger.error(f"Unhandled exception while handling message {self.message_name}. {tb.format_exc()}")
                return None
        try:
            return self.function()
        except KeyboardInterrupt as e:
            raise e
        except Exception:
            self._logger.error(f"Unhandled exception while handling message {self.message_name}. {tb.format_exc()}")
            return None

    def _requires_payload_parameter(self) -> bool:
        return self.function.__code__.co_argcount == 1
