from service import DomainCounterService
from utils import DateUtils


def test_add_domains():
    values = {"timestamp": 1608102631, "domains": {"A": 3, "B": 4}}
    timestamp = values["timestamp"]
    domains = values["domains"]

    hour_key = DateUtils.current_hour_key(timestamp=timestamp)
    min_key = DateUtils.current_minute_key(timestamp=timestamp)

    domain_counter_service = DomainCounterService()
    domain_counter_service.add_domains(timestamp=timestamp, domains=domains)
