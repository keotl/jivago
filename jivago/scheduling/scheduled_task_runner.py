import time
from datetime import datetime

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override
from jivago.lang.runnable import Runnable
from jivago.scheduling.schedule import Schedule


class ScheduledTaskRunner(Runnable):

    def __init__(self, runner_class: type, schedule: Schedule, service_locator: ServiceLocator):
        self.service_locator = service_locator
        self.runner_class = runner_class
        self.schedule = schedule
        self.shouldStop = False

    @Override
    def run(self):
        while not self.shouldStop:
            sleep_time = self.schedule.next_start_time() - datetime.utcnow()
            if sleep_time.total_seconds() > 0:
                time.sleep(sleep_time.total_seconds())
            self.service_locator.get(self.runner_class).run()
