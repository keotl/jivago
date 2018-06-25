import unittest
from datetime import datetime
from unittest import mock

from jivago.lang.registry import Registry
from jivago.lang.runnable import Runnable
from jivago.scheduling.annotations import Scheduled, Duration
from jivago.scheduling.cron_schedule import CronSchedule
from jivago.scheduling.task_schedule_initializer import TaskScheduleInitializer
from jivago.scheduling.task_scheduler import TaskScheduler

TIME_INTERVAL = Duration.MINUTE

DATE_IN_THE_FUTURE = datetime(2077, 5, 5)

CRON_STRING = "* * * * * *"


class TaskScheduleInitializerTest(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.taskScheduleInitializer = TaskScheduleInitializer(self.registry, "")
        self.taskSchedulerMock: TaskScheduler = mock.create_autospec(TaskScheduler)

    def test_givenCronString_whenCreatingSchedule_thenScheduleWithCron(self):
        self.registry.content = {}
        self.registry.register(Scheduled, ScheduledClass, arguments={"cron": CRON_STRING})

        self.taskScheduleInitializer.initialize_task_scheduler(self.taskSchedulerMock)

        runnable_class, schedule = self.taskSchedulerMock.schedule_task.call_args[0]
        self.assertIsInstance(schedule, CronSchedule)

    def test_givenCronStartDate_whenCreatingSchedule_thenDoNotScheduleBeforeStartTime(self):
        self.registry.content = {}
        self.registry.register(Scheduled, ScheduledClass, arguments={"cron": CRON_STRING, "start": DATE_IN_THE_FUTURE})

        self.taskScheduleInitializer.initialize_task_scheduler(self.taskSchedulerMock)

        runnable_class, schedule = self.taskSchedulerMock.schedule_task.call_args[0]
        self.assertTrue(schedule.next_start_time() > DATE_IN_THE_FUTURE)

    def test_givenSimpleTimeInterval_whenCreatingSchedule_thenScheduleEveryXSeconds(self):
        self.registry.content = {}
        self.registry.register(Scheduled, ScheduledClass, arguments={"every": TIME_INTERVAL})

        self.taskScheduleInitializer.initialize_task_scheduler(self.taskSchedulerMock)

        runnable_class, schedule = self.taskSchedulerMock.schedule_task.call_args[0]
        self.assertEqual(TIME_INTERVAL.interval_time_in_seconds, schedule.interval)

    def test_givenSimpleTimeIntervalWithStartTime_whenCreatingSchedule_thenDoNotScheduleBeforeStartTime(self):
        self.registry.content = {}
        self.registry.register(Scheduled, ScheduledClass, arguments={"every": TIME_INTERVAL, "start": DATE_IN_THE_FUTURE})

        self.taskScheduleInitializer.initialize_task_scheduler(self.taskSchedulerMock)

        runnable_class, schedule = self.taskSchedulerMock.schedule_task.call_args[0]
        self.assertTrue(schedule.next_start_time() > DATE_IN_THE_FUTURE)


class ScheduledClass(Runnable):
    def run(self):
        pass
