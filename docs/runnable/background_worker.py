import time

from jivago.lang.annotations import Override, BackgroundWorker, Inject
from jivago.lang.runnable import Runnable


@BackgroundWorker
class MyBackgroundWorker(Runnable):

    @Inject
    def __init__(self, component: MyComponent):
        self.component = component

    @Override
    def run(self):
        while True:
            print("hello from the background")
            time.sleep(5)
