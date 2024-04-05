from os import environ

from perfiles.infrastructure.dispatchers import (
    PerfilDemograficoIntegrationEventDispatcher,
)
from seedwork.application.handlers import Handler


class PerfilDemograficoCreatedIntegrationMessageHandler(Handler):

    @staticmethod
    def handle(event):
        dispatcher = PerfilDemograficoIntegrationEventDispatcher(event)
        dispatcher.publish(environ.get("INTEGRATION_EVENT_URL"))
