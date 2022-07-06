from queue import PriorityQueue
from typing import List, Dict

from utils import DateUtils


class DomainsCounter:

    def __init__(self):
        # domain name -> count
        self.domains_counter_dict: Dict[str: int] = {}
        self._next_time_frame: Dict[int: Dict[str, int]] = {}

    def update_all(self, timestamp: int, domain_name: str, count: int):
        if DateUtils.is_bigger_than_round_minute(timestamp):
            self._add_to_next_time_frame(timestamp, domain_name, count)
        else:
            self._update_from_next_time_frame()
            self._update_domain_count(domain_name, count)

    def _update_internal_structures(self, domain_name, count):
        prev_count = self.domains_counter_dict.get(domain_name, 0)
        new_count = prev_count + count
        self.domains_counter_dict[domain_name] = new_count

    # saving values for a minute/hours that is not yet passed
    def _add_to_next_time_frame(self, timestamp, domain_name, count):
        self._next_time_frame[timestamp][domain_name] = count

    # adding round values after time has passed
    # works fast because only not round values are added self.next_time_frame
    def _update_from_next_time_frame(self):
        for timestamp, domains_counter_dict in self._next_time_frame.items():
            if not DateUtils.is_bigger_than_round_minute(timestamp):
                for domain_name, count in domains_counter_dict.items():
                    self._update_domain_count(timestamp, domain_name, count)
                    del self._next_time_frame[timestamp]

    def get_top_domains(self, limit: int) -> List:
        self._update_from_next_time_frame()

        # top 10 domains by count
        top_domains_by_count = PriorityQueue(limit)
        for domain_name, count in self.domains_counter_dict.items():
            top_domains_by_count.put((count, domain_name))

        top_domains = []
        while not top_domains_by_count.empty():
            top_domains.append(top_domains_by_count.get())
        return top_domains
