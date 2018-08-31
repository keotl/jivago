from jivago.lang.annotations import Override
from jivago.lang.runnable import Runnable


class MyRunnableComponent(Runnable):

    @Override
    def run(self):
        print("hello!")
