

def test_add_domains():
    domain_counter_service = DomainCounterService()
    domain_counter_service.add_domains()
    assert domain_counter_service.minute_queue.qsize() == 60
    assert domain_counter_service.hour_queue.qsize() == 24
    pass

def test_get_top_10_domains_last_minutes():
    domain_counter_service = DomainCounterService()
    domain_counter_service.add_domains()
    domains = domain_counter_service.get_top_10_domains_last_minute()
    assert len(domains) == 10
    pass

def test_get_top_10_domains_last_hours():
    domain_counter_service = DomainCounterService()
    domain_counter_service.add_domains()
    domains = domain_counter_service.get_top_10_domains_last_hour()
    assert len(domains) == 10
    pass

