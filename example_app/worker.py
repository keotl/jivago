import time

from example_app.comp.beans import SomeBean
from jivago.lang.annotations import BackgroundWorker, Inject


@BackgroundWorker
class Worker(object):

    @Inject
    def __init__(self, some_bean: SomeBean):
        self.some_bean = some_bean

    def __call__(self):
        for i in range(0, 5):
            print(self.some_bean.say_hello())
            time.sleep(1)
