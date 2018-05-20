import unittest
from unittest import mock

from jivago.lang.registry import Registry
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Inject
from jivago.scheduling.annotations import Scheduled, Duration
from jivago.scheduling.scheduled_task_runner import ScheduledTaskRunner


class ScheduledTaskRunnerTest(unittest.TestCase):

    def setUp(self):
        self.service_locator = ServiceLocator()
        self.taskRunner = ScheduledTaskRunner(Registry(), "", self.service_locator)
        self.a_callable_mock = mock.MagicMock()

    def test_givenScheduledComponent_whenRunningScheduledTasks_thenInstantiateComponentWhenInvoking(self):
        self.service_locator.bind(AScheduledComponent, AScheduledComponent)

        self.taskRunner.run()


class AScheduledComponent(object):

    @Inject
    def __init__(self, a_callable_mock):
        self.a_callable_mock = a_callable_mock

    @Scheduled(every=Duration.SECOND)
    def run_scheduled(self):
        self.a_callable_mock(self.__class__)
