from datetime import datetime


class Schedule(object):

    def next_start_time(self) -> datetime:
        """Should return a datetime in UTC timezone."""
        raise NotImplementedError
