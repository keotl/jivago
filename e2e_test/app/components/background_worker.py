import anachronos

from e2e_test.testing_messages import BACKGROUND_WORKER
from jivago.lang.annotations import BackgroundWorker, Override
from jivago.lang.runnable import Runnable


@BackgroundWorker
class SomeBackgroundWorker(Runnable):

    def __init__(self):
        self.anachronos = anachronos.get_instance()

    @Override
    def run(self):
        self.anachronos.store(BACKGROUND_WORKER)
