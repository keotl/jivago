import threading
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
        self.thread_stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)

    @Override
    def run(self):
        while not self.thread_stop_event.is_set():
            sleep_time = self.schedule.next_start_time() - datetime.utcnow()
            if sleep_time.total_seconds() > 0:
                time.sleep(sleep_time.total_seconds())
            self.service_locator.get(self.runner_class).run()

    def stop(self):
        self.thread_stop_event.set()
        self.thread.join()

    def start(self):
        self.thread.start()
