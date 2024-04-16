from os import environ

from seedwork.application.handlers import Handler
from usuarios.infrastructure.dispatchers import UsuarioIntegrationEventDispatcher


class UsuarioCreatedIntegrationMessageHandler(Handler):

    @staticmethod
    def handle(event):
        dispatcher = UsuarioIntegrationEventDispatcher(event)
        dispatcher.publish(environ.get("INTEGRATION_EVENT_URL"))
