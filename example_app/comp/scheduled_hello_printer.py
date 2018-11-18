import logging

from jivago.lang.annotations import Override
from jivago.lang.registry import Singleton
from jivago.lang.runnable import Runnable
from jivago.scheduling.annotations import Scheduled, Duration


@Singleton
@Scheduled(cron="* * * * *")
class ScheduledHelloPrinter(Runnable):
    LOGGER = logging.getLogger("HelloPrinter")

    def __init__(self):
        self.LOGGER.info("created a new scheduled hello printer")

    @Override
    def run(self):
        self.LOGGER.info("hello !")


@Scheduled(every=Duration.SECOND)
class RegularIntervalScheduledHelloPrinter(Runnable):
    LOGGER = logging.getLogger("ScheduledHelloPrinter")

    @Override
    def run(self):
        self.LOGGER.info("Hello every second!")
