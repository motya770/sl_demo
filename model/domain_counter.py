from utils import DateUtils


class DomainCounter:

    def __init__(self):
        self.name = None
        self.hours_count = {}
        self.minutes_count = {}

    def add_count(self, count: int, timestamp: int):
        hour_key = DateUtils.current_hour_key(timestamp)
        minute_key = DateUtils.current_minute_key(timestamp)
        self.hours_count[hour_key] = self.hours_count.get(hour_key, 0) + count
        self.minutes_count[minute_key] = self.minutes_count.get(minute_key, 0) + count



