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
        domains = self.domain_counter_service.get_top_10_domains_last_minute()
        return json({"domains": domains})

    def get_top_10_domains_last_hours(self, request):
        domains = self.domain_counter_service.get_top_10_domains_last_hour()
        return json({"domains": domains})

    def add_domains(self, request):
        self.domain_counter_service.add_domains()
        return json({"result": "domains added"})


def create_domain_counter_controller(domain_counter_controller: DomainCounterController, app):
    domain_counter_bp = Blueprint('domain_counter')

    @domain_counter_bp.route('/domain/top-10-domains-minute', methods=['GET'])
    def decorated_domain_counter_minutes(request):
        return domain_counter_controller.get_top_10_domains_last_minutes(request)

    @domain_counter_bp.route('/domain/top-10-domains-hour', methods=['GET'])
    def decorated_domain_counter_hours(request):
        return domain_counter_controller.get_top_10_domains_last_hours(request)

    @domain_counter_bp.route('/domain', methods=['PUT'])
    def decorated_domain_counter_add_domains(request):
        return domain_counter_controller.add_domains(request)

    app.blueprint(domain_counter_bp)
