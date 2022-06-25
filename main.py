import asyncio
from injector import Injector
from sanic import Sanic

from api import DomainCounterController, create_domain_counter_controller

if __name__ == "__main__":
    app = Sanic("SlackPathDemoApp")
    ioc_container = Injector()

    domain_counter_controller = ioc_container.get(DomainCounterController)
    create_domain_counter_controller(domain_counter_controller, app)

    app.run()