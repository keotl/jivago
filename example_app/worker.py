import time

from example_app.comp.beans import SomeBean
from jivago.lang.annotations import BackgroundWorker, Inject, Override
from jivago.lang.runnable import Runnable


@BackgroundWorker
class Worker(Runnable):

    @Inject
    def __init__(self, some_bean: SomeBean):
        self.some_bean = some_bean

    @Override
    def run(self):
        for i in range(0, 5):
            print(self.some_bean.say_hello())
            time.sleep(1)
