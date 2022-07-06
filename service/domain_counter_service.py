from typing import List, Dict
from injector import singleton, inject
from utils import DateUtils
from model import DomainsCounter


@singleton
class DomainCounterService:

    @inject
    def __init__(self):
        # dict by time with dict by domain name with count
        self.min_domain_counter_holder: Dict[str: DomainsCounter] = {}
        self.hour_domain_counter_holder: Dict[str: DomainsCounter] = {}

    def add_domains(self, timestamp: int, domains: List[str]):
        min_key = DateUtils.current_minute_key(timestamp)
        hour_key = DateUtils.current_hour_key(timestamp)

        for domain_name, count in domains.items():
            self._add_domain(time_key=min_key, timestamp=timestamp,
                             domain_counter_holder_dict=self.min_domain_counter_holder,
                             count=count, domain_name=domain_name)

            self._add_domain(time_key=hour_key, timestamp=timestamp,
                             domain_counter_holder_dict=self.hour_domain_counter_holder,
                             count=count, domain_name=domain_name)

    def _add_domain(self, time_key: str, timestamp: int, domain_counter_holder_dict: Dict, count: int,
                    domain_name: str):
        domains_counter: DomainsCounter = domain_counter_holder_dict.get(time_key, None)
        if domains_counter is None:
            domains_counter = DomainsCounter()
            domain_counter_holder_dict[time_key] = domains_counter
        domains_counter.update_all(timestamp=timestamp, domain_name=domain_name, count=count)

    # 0(1)
    def _get_top_domains(self, limit: int, domain_counter_holder_dict: Dict, time_key: str):
        domain_counter: DomainsCounter = domain_counter_holder_dict.get(time_key)
        if domain_counter is None:
            return None
        return domain_counter.get_top_domains(limit)

    def get_top_10_domains_hour(self) -> List:
        hour_key = DateUtils.round_hour_key()
        return self._get_top_domains(10, self.hour_domain_counter_holder, hour_key)

    def get_top_10_domains_minute(self) -> List:
        minute_key = DateUtils.round_minute_key()
        return self._get_top_domains(10, self.min_domain_counter_holder, minute_key)
