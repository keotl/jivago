from datetime import datetime

from croniter import croniter

from jivago.lang.annotations import Override
from jivago.scheduling.schedule import Schedule


class CronSchedule(Schedule):

    def __init__(self, cron_string: str):
        self.iterator = croniter(cron_string)

    @Override
    def next_start_time(self) -> datetime:
        return self.iterator.get_next(ret_type=datetime)
