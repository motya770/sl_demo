from typing import List, Dict
from injector import singleton, inject
from utils import DateUtils


@singleton
class DomainCounterService:

    @inject
    def __init__(self):
        # dict by time with dict by domain name with count
        self.min_domain_counter_holder = {str: Dict[str, int]}
        self.hour_domain_counter_holder = {str: Dict[str, int]}

    def add_domains(self, domains: List[str]):
        values = {"timestamp": 1608102631, "domains": {"A": 3, "B": 4}}
        timestamp = values["timestamp"]
        domains = values["domains"]

        min_key = DateUtils.current_minute_key(timestamp)
        hour_key = DateUtils.current_hour_key(timestamp)

        for domain_name, count in domains.items():
            self._add_domain(time_key=min_key, domain_counter_holder_dict=self.min_domain_counter_holder,
                             count=count, domain_name=domain_name)

            self._add_domain(time_key=hour_key, domain_counter_holder_dict=self.hour_domain_counter_holder,
                             count=count, domain_name=domain_name)

    def _add_domain(self, time_key: str, domain_counter_holder_dict: Dict, count: int, domain_name: str):
        counter_dict = domain_counter_holder_dict.get(time_key, None)
        if counter_dict is None:
            counter_dict = {}
            self.domain_counter_holder_dict[time_key] = counter_dict
        domain_count = counter_dict.get(domain_name, 0)
        counter_dict[domain_name] = domain_count + count

    # 0 n log n - only for slice of 1 minute
    def _get_top_domains_last_minute(self, limit: int):
        min_counter_dict = self.min_domain_counter_holder.get(DateUtils.round_minute_key(), None)
        return self._sorted_dict_by_limit(limit, min_counter_dict)

    # n log n
    def _sorted_dict_by_limit(self, limit: 10, counter_dict: Dict[str, int]):
        if counter_dict is None:
            return None

        result = []
        # sort by value (by count for specific domain)
        for k, v in sorted(counter_dict.items(), key=lambda item: item[1]):
            result.append({k, v})
            if len(result) == limit:
                break

        return result

    # 0 n log n - only for slice of 1 minute
    def _get_top_domains_last_hour(self, limit: int):
        hour_counter_dict = self.hour_domain_counter_holder.get(DateUtils.round_hour_key())
        return self._sorted_dict_by_limit(limit, hour_counter_dict)

    # 0(1)
    def get_top_10_domains_last_hour(self) -> List:
        return self._get_top_domains_last_hour(10)

    # 0(1)
    def get_top_10_domains_last_minute(self) -> List:
        return self._get_top_domains_last_minute(10)
