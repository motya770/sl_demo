from typing import List, Dict
from injector import singleton, inject
from utils import DateUtils


@singleton
class DomainCounterService:

    @inject
    def __init__(self):
        self.min_domain_counter_holder = {}
        self.hour_domain_counter_holder = {}

    def add_domains(self, domains: List[str]):
        values = {"timestamp": 1608102631, "domains": {"A": 3, "B": 4}}
        timestamp = values["timestamp"]
        domains = values["domains"]
        for domain_name, count in domains.items():
            min_key = DateUtils.current_minute_key(timestamp)
            min_counter_dict = self.min_domain_counter_holder.get(min_key, None)
            if min_counter_dict is None:
                min_counter_dict = {}
                self.min_domain_counter_holder[min_key] = min_counter_dict

            min_domain_count = min_counter_dict.get(domain_name, 0)
            min_counter_dict[domain_name] = min_domain_count + count

            hour_key = DateUtils.current_hour_key(timestamp)
            hour_counter_dict = self.hour_domain_counter_holder.get(hour_key, None)
            if hour_counter_dict is None:
                hour_counter_dict = {}
                self.hour_domain_counter_holder[hour_key] = hour_counter_dict

            hour_domain_count = hour_counter_dict.get(domain_name, 0)
            hour_counter_dict[domain_name] = hour_domain_count + count

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
