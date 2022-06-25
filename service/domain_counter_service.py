from typing import List

from injector import singleton, inject
from model import DomainCounter
from utils import DateUtils


@singleton
class DomainCounterService:

    @inject
    def __init__(self):
        self.domain_counter_holder = {}

    # 0(n) * 0(1)
    def add_domains(self):
        values = {"timestamp": 1608102631, "domains": {"A": 3, "B": 4}}
        timestamp = values["timestamp"]
        domains = values["domains"]
        for domain_name, count in domains.items():
            domain_counter = self.domain_counter_holder.get(domain_name, None)
            if domain_counter is None:
                domain_counter = DomainCounter(name=domain_name)
                self.domain_counter_holder[domain_name] = domain_counter

            domain_counter.add_count(timestamp, count)

    # 0(1)
    def get_top_10_domains_last_minutes(self) -> List:
        result = []
        minute_key = DateUtils.round_minute_key()
        for domain_name, domain_counter in self.domain_counter_holder.items():
            count = domain_counter.minutes_count.get(minute_key, 0)
            result.append({"domain": domain_name, "count": count})
        return result

    # 0(1)
    def get_top_10_domains_last_hours(self) -> List:
        result = []
        hour_key = DateUtils.round_hour_key()
        for domain_name, domain_counter in self.domain_counter_holder.items():
            count = domain_counter.hour_count.get(hour_key, 0)
            result.append({"domain": domain_name, "count": count})
        return result
