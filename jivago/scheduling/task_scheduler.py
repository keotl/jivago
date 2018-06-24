from threading import Thread, Lock

from jivago.inject.service_locator import ServiceLocator
from jivago.scheduling.schedule import Schedule
from jivago.scheduling.scheduled_task_runner import ScheduledTaskRunner


class TaskScheduler(object):

    def __init__(self, service_locator: ServiceLocator):
        self.service_locator = service_locator
        self.threads = []
        self.lock = Lock()

    def schedule_task(self, runnable_class: type, schedule: Schedule):
        self.lock.acquire()
        task_runner = ScheduledTaskRunner(runnable_class, schedule, self.service_locator)
        thread = Thread(target=task_runner.run)
        thread.start()
        self.threads.append(thread)
        self.lock.release()
