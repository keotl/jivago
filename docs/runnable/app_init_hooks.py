from jivago.config.startup_hooks import PreInit, Init, PostInit, PreShutdown
from jivago.lang.annotations import Override
from jivago.lang.runnable import Runnable


@PreInit
class FirstHook(Runnable):

    @Override
    def run(self):
        print("First!")


@Init
class SecondHook(Runnable):

    @Override
    def run(self):
        print("Second!")


@PostInit
class ThirdHook(Runnable):

    @Override
    def run(self):
        print("Third!")

@PreShutdown
class ShutdownHook(Runnable):

    @Override
    def run(self):
        print("Cleaning up before shutting down.")
