from typing import List

from injector import singleton, inject


@singleton
class DomainCounterService:

    @inject
    def __init__(self):
        self.domain_counter_holder = None

    def add_domains(self):
        pass

    def get_top_10_domains_last_minutes(self) -> List:
        pass

    def get_top_10_domains_last_hours(self) -> List:
        pass
