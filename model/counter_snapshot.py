
class CounterShapshot:
    def __init__(self, prev_round_min_count, round_min_count,
                 prev_round_hour_count, round_hour_count):
        self.prev_round_min_count = prev_round_min_count
        self.prev_hour_count = prev_round_hour_count
        self.round_min_count = round_min_count
        self.round_hour_count = round_hour_count

