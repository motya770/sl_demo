from typing import List, Dict
from injector import singleton, inject
from model import DomainCounter
from model.counter_snapshot import CounterShapshot
from sortedcontainers import SortedDict


@singleton
class DomainCounterService:

    @inject
    def __init__(self):
        self.domain_counter_holder = {}
        self.minute_queue = SortedDict()
        self.hour_queue = SortedDict()

    # 0(n) * 0(log N)
    def add_domains(self):
        values = {"timestamp": 1608102631, "domains": {"A": 3, "B": 4}}
        timestamp = values["timestamp"]
        domains = values["domains"]
        for domain_name, count in domains.items():
            domain_counter: DomainCounter = self.domain_counter_holder.get(domain_name, None)
            if domain_counter is None:
                domain_counter = DomainCounter(name=domain_name)
                self.domain_counter_holder[domain_name] = domain_counter

            counter_snapshot = domain_counter.add_count(timestamp, count)
            self.add_to_minute_queue(domain_name, counter_snapshot)
            self.add_to_hour_queue(domain_name, counter_snapshot)

    # Log N
    def add_to_minute_queue(self, domain_name: str, counter_snapshot: CounterShapshot):
        # queue is reversed
        prev_min_domains: Dict = self.minute_queue.get(-counter_snapshot.prev_round_min)
        # remove from old position in queue for previous calculation
        if prev_min_domains is not None and len(prev_min_domains) > 0:
            del prev_min_domains[domain_name]

        # add to new position in queue
        min_domains = self.minute_queue.get(-counter_snapshot.round_min_count)
        if min_domains is None:
            min_domains = {}
            self.minute_queue.put(-counter_snapshot.round_min_count, min_domains)
        min_domains[domain_name] = domain_name

    def add_to_minute_queue(self, domain_name: str, counter_snapshot: CounterShapshot):
        prev_hour_domains: Dict = self.hour_queue.get(-counter_snapshot.prev_round_hour)
        # remove from old position in queue for previous calculation
        if prev_hour_domains is not None and len(prev_hour_domains) > 0:
            del prev_hour_domains[domain_name]

        # add to new position in queue
        hour_domains = self.hour_queue.get(-counter_snapshot.round_hour_count)
        if hour_domains is None:
            hour_domains = {}
            self.hour_queue.put(-counter_snapshot.round_hour_count, hour_domains)
        hour_domains[domain_name] = domain_name

    # looks like 0(n^2) but actually close to 0(1)
    def _get_top_domains_last_minute(self, limit: int):
        result = []
        counter = 0
        top_counters_dict: Dict = self.minute_queue.islice(0, limit)
        for domain_count, domain_names_dict in top_counters_dict:
            for domain_name in domain_names_dict.keys():
                result.append({"domain": domain_name, "count": domain_count})
                counter += 1
                if counter == limit:
                    return result
        return result

    # looks like 0(n^2) but actually close to 0(1)
    def _get_top_domains_last_hour(self, limit: int):
        result = []
        counter = 0
        top_counters_dict: Dict = self.hour_queue.islice(0, limit)
        for domain_count, domain_names_dict in top_counters_dict.items():
            for domain_name in domain_names_dict.keys():
                result.append({"domain": domain_name, "count": domain_count})
                counter += 1
                if counter == limit:
                    return result
        return result

    # 0(1)
    def get_top_10_domains_last_hour(self) -> List:
        return self._get_top_domains_last_hour(10)

    # 0(1)
    def get_top_10_domains_last_minute(self) -> List:
        return self._get_top_domains_last_minute(10)
