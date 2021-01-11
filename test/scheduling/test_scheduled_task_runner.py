import unittest
import time
from datetime import datetime
from unittest import mock

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override
from jivago.lang.runnable import Runnable
from jivago.scheduling.schedule import Schedule
from jivago.scheduling.scheduled_task_runner import ScheduledTaskRunner


class ScheduledTaskRunnerTests(unittest.TestCase):

    def setUp(self):
        self.service_locator = ServiceLocator()
        self.service_locator.bind(SomeScheduledTask, SomeScheduledTask)
        self.service_locator.bind(SomeCrashingTask, SomeCrashingTask)
        self.service_locator.bind(SomeTaskCrashingOnCleanup, SomeTaskCrashingOnCleanup)
        self.schedule_mock: Schedule = mock.create_autospec(Schedule)
        self.schedule_mock.next_start_time.return_value = datetime.now()

    def test_run_scheduled_task(self):
        self.runner = ScheduledTaskRunner(SomeScheduledTask, self.schedule_mock, self.service_locator)

        self.runner.start()

        self.assertTrue(SomeScheduledTask.was_called)

    def test_givenUncaughtException_whenExecuting_shouldNotCrash(self):
        self.runner = ScheduledTaskRunner(SomeCrashingTask, self.schedule_mock, self.service_locator)

        self.runner.start()
        time.sleep(0.05)

        self.assertTrue(SomeCrashingTask.times_called > 1)

    def test_givenUncaughtException_whenCleaningUp_shouldNotCrash(self):
        self.runner = ScheduledTaskRunner(SomeTaskCrashingOnCleanup, self.schedule_mock, self.service_locator)

        self.runner.start()
        self.runner.stop()

        self.assertTrue(SomeTaskCrashingOnCleanup.run_called)
        self.assertTrue(SomeTaskCrashingOnCleanup.cleanup_called)

    def tearDown(self):
        self.runner.stop()


class SomeScheduledTask(Runnable):
    was_called = False

    @Override
    def run(self):
        SomeScheduledTask.was_called = True


class SomeCrashingTask(Runnable):
    times_called = 0

    @Override
    def run(self):
        SomeCrashingTask.times_called += 1

        if SomeCrashingTask.times_called == 1:
            raise Exception("Error!!")

class SomeTaskCrashingOnCleanup(Runnable):
    cleanup_called = False
    run_called = False
    def run(self):
        SomeTaskCrashingOnCleanup.run_called = True

    def cleanup(self):
        SomeTaskCrashingOnCleanup.cleanup_called = True
        raise Exception("Error!")


