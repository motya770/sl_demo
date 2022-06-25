from sanic import Blueprint
from sanic.response import json
from injector import inject, singleton

from service import DomainCounterService


@singleton
class DomainCounterController:

    @inject
    def __init__(self, domain_counter_service: DomainCounterService):
        self.domain_counter_service = domain_counter_service

    def get_top_10_domains_last_minutes(self, request):
        domains = self.domain_counter_service.get_top_10_domains_last_minutes()
        return json({"domains": domains})

    def get_top_10_domains_last_hours(self, request):
        domains = self.domain_counter_service.get_top_10_domains_last_hours()
        return json({"domains": domains})


def create_domain_counter_controller(domain_counter_controller: DomainCounterController, app):
    domain_counter_bp = Blueprint('domain_counter')

    @domain_counter_bp.route('/domains/top-10-domains-minutes')
    def decorated_domain_counter_minutes(request):
        return domain_counter_controller.get_top_10_domains_last_minutes(request)

    @domain_counter_bp.route('/domains/top-10-domains-hours')
    def decorated_domain_counter_hours(request):
        return domain_counter_controller.get_top_10_domains_last_hours(request)

    app.blueprint(domain_counter_bp)
