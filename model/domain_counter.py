from queue import PriorityQueue

from model.counter_snapshot import CounterShapshot
from utils import DateUtils


class DomainCounter:

    def __init__(self):
        self.name = None
        # TODO add clean methods
        self.hours_count = {}
        self.minutes_count = {}

    def add_count(self, count: int, timestamp: int):
        hour_key = DateUtils.current_hour_key(timestamp)
        minute_key = DateUtils.current_minute_key(timestamp)

        prev_round_hour_count = self.hours_count.get(hour_key, 0)
        prev_round_min_count = self.minutes_count.get(minute_key, 0)
        round_hour_count = prev_round_hour_count + count
        round_min_count = prev_round_min_count + count

        self.hours_count[hour_key] = round_hour_count
        self.minutes_count[minute_key] = round_min_count

        counter_snapshot = CounterShapshot(prev_round_min_count, round_min_count,
                                           prev_round_hour_count, round_hour_count)
        return counter_snapshot
