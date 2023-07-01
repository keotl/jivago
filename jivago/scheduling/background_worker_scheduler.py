import logging
import traceback
from threading import Thread
from typing import Iterable
from jivago.lang.annotations import Override
from jivago.lang.runnable import Runnable
from jivago.lang.stream import Stream


class BackgroundWorkerScheduler(object):

    def __init__(self, runnables: Iterable[Runnable]) -> None:
        self._threads = Stream(runnables) \
            .map(lambda r: BackgroundWorkerRunner(r)) \
            .map(lambda worker: Thread(target=worker.run, daemon=True))

    def start(self):
        for t in self._threads:
            t.start()


class BackgroundWorkerRunner(Runnable):

    def __init__(self, wrapped: Runnable) -> None:
        self._wrapped = wrapped
        self._logger = logging.getLogger(self.__class__.__name__)

    @Override
    def run(self):
        try:
            self._wrapped.run()
            self._logger.info(f"Background worker '{self._wrapped.__class__}' exited cleanly.")
        except Exception as e:
            self._logger.error(f"Background worker '{self._wrapped.__class__}' crashed due to uncaught exception!",
                               traceback.format_exc())
            raise e
