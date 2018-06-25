from datetime import datetime, timedelta

from jivago.lang.annotations import Override
from jivago.scheduling.annotations import _Interval
from jivago.scheduling.schedule import Schedule


class RegularIntervalSchedule(Schedule):

    def __init__(self, time_interval: _Interval, start_time: datetime = None):
        self.interval = time_interval.interval_time_in_seconds
        self.next_time = start_time if start_time else datetime.utcnow()

    def increment(self):
        self.next_time += timedelta(seconds=self.interval)

    @Override
    def next_start_time(self) -> datetime:
        self.increment()
        return self.next_time
