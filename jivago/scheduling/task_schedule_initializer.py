from jivago.lang.registry import Registry
from jivago.scheduling.annotations import Scheduled
from jivago.scheduling.cron_schedule import CronSchedule
from jivago.scheduling.regular_interval_schedule import RegularIntervalSchedule
from jivago.scheduling.task_scheduler import TaskScheduler


class TaskScheduleInitializer(object):

    def __init__(self, registry: Registry, root_package_name: str):
        self.registry = registry
        self.root_package_name = root_package_name

    def initialize_task_scheduler(self, task_scheduler: TaskScheduler):

        for registration in self.registry.get_annotated_in_package(Scheduled, self.root_package_name):
            schedule = None
            start_time = registration.arguments.get('start')

            if registration.arguments.get('cron'):
                schedule = CronSchedule(registration.arguments['cron'], start_time)

            if registration.arguments.get('every'):
                schedule = RegularIntervalSchedule(registration.arguments['every'], start_time)

            task_scheduler.schedule_task(registration.registered, schedule)
