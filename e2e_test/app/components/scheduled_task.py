from anachronos import Anachronos
from e2e_test.testing_messages import SCHEDULED
from jivago.lang.annotations import Override, Inject
from jivago.lang.runnable import Runnable
from jivago.scheduling.annotations import Scheduled, Duration


@Scheduled(every=Duration.SECOND)
class ScheduledTaskRunner(Runnable):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @Override
    def run(self):
        self.anachronos.store(SCHEDULED)
