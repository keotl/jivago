from datetime import datetime

from croniter import croniter

from jivago.lang.annotations import Override
from jivago.scheduling.schedule import Schedule


class CronSchedule(Schedule):

    def __init__(self, cron_string: str, start_time: datetime):
        if start_time:
            self.iterator = croniter(cron_string, start_time=start_time.timestamp())
        else:
            self.iterator = croniter(cron_string)

    @Override
    def next_start_time(self) -> datetime:
        return self.iterator.get_next(ret_type=datetime)
