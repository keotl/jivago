from jivago.config.startup_hooks import PreInit, Init, PostInit
from jivago.lang.annotations import Override
from jivago.lang.runnable import Runnable


@PreInit
class PreInitMessage(Runnable):

    @Override
    def run(self):
        print("PreInit! The app will soon be up and running!")


@Init
class InitMessage(Runnable):

    @Override
    def run(self):
        print("Init! The app is starting up!")


@PostInit
class PostInitMessage(Runnable):

    @Override
    def run(self):
        print("PostInit! The app is now ready!")
