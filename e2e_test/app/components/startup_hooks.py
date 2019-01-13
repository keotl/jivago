import anachronos
from anachronos import Anachronos
from e2e_test.testing_messages import PREINIT, INIT, POSTINIT
from jivago.config.startup_hooks import PreInit, Init, PostInit
from jivago.lang.annotations import Inject, Override
from jivago.lang.runnable import Runnable


@PreInit
class PreInitHook(Runnable):

    def __init__(self):
        self.anachronos = anachronos.get_instance()

    @Override
    def run(self):
        self.anachronos.store(PREINIT)


@Init
class InitHook(Runnable):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @Override
    def run(self):
        self.anachronos.store(INIT)


@PostInit
class PreInitHook(Runnable):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @Override
    def run(self):
        self.anachronos.store(POSTINIT)
