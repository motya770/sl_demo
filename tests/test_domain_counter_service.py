import datetime

from service import DomainCounterService
from utils import DateUtils


def test_add_domains():
    timestamp = int(datetime.datetime.utcnow().timestamp())
    values = {"timestamp": timestamp, "domains": {"A": 3, "B": 4}}
    timestamp = values["timestamp"]
    domains = values["domains"]

    hour_key = DateUtils.current_hour_key(timestamp=timestamp)
    min_key = DateUtils.current_minute_key(timestamp=timestamp)

    domain_counter_service = DomainCounterService()
    domain_counter_service.add_domains(timestamp=timestamp, domains=domains)

    resp = domain_counter_service.get_top_10_domains_hour()
    print(resp)
