from seedwork.application.handlers import Handler
from usuarios.infrastructure.dispatchers import UsuarioIntegrationEventDispatcher


class UsuarioCreatedIntegrationMessageHandler(Handler):

    @staticmethod
    def handle(event):
        dispatcher = UsuarioIntegrationEventDispatcher(event)
        dispatcher.publish("usuarios-events")