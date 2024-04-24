from os import environ

from perfiles.infrastructure.dispatchers import (
    PerfilDemograficoIntegrationEventDispatcher,
)
from seedwork.application.handlers import Handler


class PerfilDemograficoModifiedIntegrationMessageHandler(Handler):

    @staticmethod
    def handle(event):
        dispatcher = PerfilDemograficoIntegrationEventDispatcher(event)
        dispatcher.publish(environ.get("INTEGRATION_EVENT_URL"))
