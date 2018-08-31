from jivago.lang.annotations import Override
from jivago.lang.runnable import Runnable
from jivago.scheduling.annotations import Scheduled, Duration


@Scheduled(every=Duration.HOUR)
class ScheduledTask(Runnable):

    @Override
    def run(self):
        print("hello")
